# BowlsAce API Integration Guide

This document provides guidance on integrating the BowlsAce API with your Next.js frontend application.

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
Most endpoints require authentication. Add the JWT token to your API requests:
```typescript
const headers = {
  'Authorization': `Bearer ${token}`,
  'Content-Type': 'application/json'
};
```

## API Endpoints Integration Guide

### 1. Drill Management (Admin Dashboard)

#### Drill List Screen (/admin/drills)
```typescript
// Get all drills with optional filtering
GET /api/v1/drill/
Query parameters:
- skip (optional): number (pagination offset)
- limit (optional): number (pagination limit)
- search (optional): string (search by name/description)
- difficulty (optional): number (1-5)

// Example integration in Next.js
const fetchDrills = async () => {
  const response = await fetch(`${API_URL}/drill/?limit=10&skip=0`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const drills = await response.json();
  return drills;
};
```

#### Create Drill Form
```typescript
// Create a new drill
POST /api/v1/drill/
Body: {
  name: string,
  description: string,
  target_score: number (1-10),
  difficulty: number (1-5),
  drill_type: string ('DRAW' | 'DRIVE' | 'WEIGHT_CONTROL' | 'POSITION' | 'MIXED'),
  duration_minutes: number
}

// Example integration
const createDrill = async (drillData) => {
  const response = await fetch(`${API_URL}/drill/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(drillData)
  });
  const newDrill = await response.json();
  return newDrill;
};
```

#### Edit Drill Screen (/admin/drills/[id])
```typescript
// Get specific drill
GET /api/v1/drill/{drill_id}

// Update drill
PUT /api/v1/drill/{drill_id}
Body: {
  name?: string,
  description?: string,
  target_score?: number,
  difficulty?: number,
  drill_type?: string,
  duration_minutes?: number
}

// Delete drill
DELETE /api/v1/drill/{drill_id}
```

### 2. Practice Session Management

#### Start Practice Screen (/practice/new)
```typescript
// Create a new practice session
POST /api/v1/practice/sessions
Body: {
  drill_ids: number[]  // IDs of selected drills
}

// Example integration
const startPractice = async (selectedDrills) => {
  const response = await fetch(`${API_URL}/practice/sessions`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ drill_ids: selectedDrills })
  });
  const session = await response.json();
  return session;
};
```

#### Practice Session Screen (/practice/[sessionId])
```typescript
// Get session details
GET /api/v1/practice/sessions/{session_id}

// Record a shot
POST /api/v1/practice/sessions/{session_id}/shots
Body: {
  drill_id: number,
  score: number,
  notes?: string
}

// Example integration for recording shots
const recordShot = async (sessionId, shotData) => {
  const response = await fetch(`${API_URL}/practice/sessions/${sessionId}/shots`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(shotData)
  });
  const shot = await response.json();
  return shot;
};
```

#### Practice History Screen (/practice/history)
```typescript
// Get practice session history
GET /api/v1/practice/sessions
Query parameters:
- skip?: number
- limit?: number
- start_date?: string (ISO date)
- end_date?: string (ISO date)

// Example integration with date filtering
const fetchPracticeHistory = async (startDate, endDate) => {
  const params = new URLSearchParams({
    start_date: startDate.toISOString(),
    end_date: endDate.toISOString(),
    limit: '10'
  });
  const response = await fetch(`${API_URL}/practice/sessions?${params}`, {
    headers: { Authorization: `Bearer ${token}` }
  });
  const history = await response.json();
  return history;
};
```

### 3. Dashboard Integration

#### Main Dashboard Screen (/dashboard)
```typescript
// Get dashboard statistics
GET /api/v1/dashboard/stats
Returns:
- Total practice sessions
- Recent scores
- Improvement trends
- Practice time statistics

// Get drill performance stats
GET /api/v1/dashboard/drill-stats
Returns:
- Performance by drill type
- Best/worst drills
- Recent drill completion rates

// Example integration for dashboard
const fetchDashboardData = async () => {
  const [statsResponse, drillStatsResponse] = await Promise.all([
    fetch(`${API_URL}/dashboard/stats`, {
      headers: { Authorization: `Bearer ${token}` }
    }),
    fetch(`${API_URL}/dashboard/drill-stats`, {
      headers: { Authorization: `Bearer ${token}` }
    })
  ]);

  const stats = await statsResponse.json();
  const drillStats = await drillStatsResponse.json();

  return {
    generalStats: stats,
    drillPerformance: drillStats
  };
};
```

## Recommended Data Flow Architecture

1. **State Management**:
   ```typescript
   // Use React Query for API data management
   import { useQuery, useMutation } from 'react-query';

   // Example for drills list
   const useDrills = () => {
     return useQuery('drills', fetchDrills);
   };

   // Example for creating a drill
   const useCreateDrill = () => {
     return useMutation(createDrill);
   };
   ```

2. **Error Handling**:
   ```typescript
   // Create a common error handler
   const handleApiError = (error) => {
     if (error.status === 401) {
       // Handle unauthorized access
       router.push('/login');
     } else if (error.status === 404) {
       // Handle not found
       toast.error('Resource not found');
     } else {
       // Handle other errors
       toast.error('An error occurred. Please try again.');
     }
   };
   ```

3. **Loading States**:
   ```typescript
   // Example component with loading state
   const DrillsList = () => {
     const { data, isLoading, error } = useDrills();

     if (isLoading) return <LoadingSpinner />;
     if (error) return <ErrorMessage error={error} />;

     return (
       <div>
         {data.map(drill => (
           <DrillCard key={drill.id} drill={drill} />
         ))}
       </div>
     );
   };
   ```

## WebSocket Integration (Real-time Features)

For real-time features like live practice session updates:

```typescript
// Initialize WebSocket connection
const initializeWebSocket = (sessionId: string) => {
  const ws = new WebSocket(`ws://localhost:8000/ws/practice/${sessionId}`);
  
  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    // Handle real-time updates
    switch (data.type) {
      case 'shot_recorded':
        updateShotsList(data.shot);
        break;
      case 'session_completed':
        handleSessionComplete(data.session);
        break;
    }
  };

  return ws;
};
```

## Recommended Folder Structure

```
src/
  api/
    drills.ts      # Drill-related API calls
    practice.ts    # Practice session API calls
    dashboard.ts   # Dashboard API calls
  hooks/
    useDrills.ts
    usePractice.ts
    useDashboard.ts
  components/
    drills/
      DrillCard.tsx
      DrillForm.tsx
    practice/
      SessionTimer.tsx
      ShotRecorder.tsx
    dashboard/
      StatsCard.tsx
      PerformanceChart.tsx
  pages/
    admin/
      drills/
        index.tsx   # Drills list
        [id].tsx    # Edit drill
        new.tsx     # Create drill
    practice/
      new.tsx      # Start practice
      [id].tsx     # Active session
      history.tsx  # Practice history
    dashboard.tsx  # Main dashboard
```

## API Response Types

```typescript
// Add these types to your project for better type safety
interface Drill {
  id: number;
  name: string;
  description: string;
  target_score: number;
  difficulty: number;
  drill_type: 'DRAW' | 'DRIVE' | 'WEIGHT_CONTROL' | 'POSITION' | 'MIXED';
  duration_minutes: number;
  created_at: string;
  session_id: number | null;
}

interface PracticeSession {
  id: number;
  drills: Drill[];
  shots: Shot[];
  started_at: string;
  completed_at: string | null;
  total_score: number;
}

interface Shot {
  id: number;
  session_id: number;
  drill_id: number;
  score: number;
  notes?: string;
  created_at: string;
}

interface DashboardStats {
  total_sessions: number;
  recent_scores: number[];
  improvement_trend: {
    date: string;
    score: number;
  }[];
  practice_time: {
    total_minutes: number;
    sessions_this_week: number;
  };
}
```
