"""
Fixed admin_dashboard function with proper error handling
"""

@router.get("/", response_class=HTMLResponse, name="admin_dashboard")
async def admin_dashboard(
    request: Request, 
    auth=Depends(require_admin_auth),
    db: AsyncSession = Depends(get_db)
):
    import logging
    logger = logging.getLogger(__name__)
    
    if isinstance(auth, RedirectResponse):
        return auth
    
    # Initialize default values for all stats
    stats = {
        "total_users": 0,
        "new_users_today": 0,
        "total_sessions": 0,
        "new_sessions_today": 0,
        "total_shots": 0,
        "new_shots_today": 0,
        "active_challenges": 0,
        "completed_challenges_today": 0
    }
    
    # Initialize default chart data
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
    user_counts = [0, 0, 0, 0, 0, 0]
    shot_types = ["Draw", "Drive", "Weight"]
    accuracies = [0, 0, 0]
    
    # Default empty activities
    recent_activities = []
    
    try:
        # Get live statistics
        today = datetime.now()
        today_start = datetime(today.year, today.month, today.day)

        # User statistics
        try:
            stats["total_users"] = await crud_user.get_count(db)
        except Exception as e:
            logger.error(f"Error fetching total users: {e}")
            
        try:
            stats["new_users_today"] = await crud_user.get_count(
                db, 
                created_at_after=today_start
            )
        except Exception as e:
            logger.error(f"Error fetching new users today: {e}")

        # Session statistics
        try:
            stats["total_sessions"] = await crud_practice.get_session_count(db)
        except Exception as e:
            logger.error(f"Error fetching total sessions: {e}")
            
        try:
            stats["new_sessions_today"] = await crud_practice.get_session_count(
                db,
                created_at_after=today_start
            )
        except Exception as e:
            logger.error(f"Error fetching new sessions today: {e}")

        # Shot statistics
        try:
            stats["total_shots"] = await crud_practice.get_shot_count(db)
        except Exception as e:
            logger.error(f"Error fetching total shots: {e}")
            
        try:
            stats["new_shots_today"] = await crud_practice.get_shot_count(
                db,
                created_at_after=today_start
            )
        except Exception as e:
            logger.error(f"Error fetching new shots today: {e}")

        # Challenge statistics
        try:
            stats["active_challenges"] = await crud_challenge.get_count(
                db,
                status="active"
            )
        except Exception as e:
            logger.error(f"Error fetching active challenges: {e}")
            
        try:
            stats["completed_challenges_today"] = await crud_challenge.get_count(
                db,
                status="completed",
                completed_at_after=today_start
            )
        except Exception as e:
            logger.error(f"Error fetching completed challenges today: {e}")

        # User growth chart data (last 6 months)
        try:
            months = []
            user_counts = []
            for i in range(5, -1, -1):
                month_date = today - timedelta(days=i*30)
                months.append(month_date.strftime("%b"))
                try:
                    count = await crud_user.get_count(
                        db,
                        created_at_before=month_date
                    )
                    user_counts.append(count)
                except Exception as e:
                    logger.error(f"Error fetching user count for month {month_date.strftime('%b')}: {e}")
                    user_counts.append(0)
        except Exception as e:
            logger.error(f"Error generating user growth chart data: {e}")
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]  # Reset to defaults
            user_counts = [0, 0, 0, 0, 0, 0]  # Reset to defaults

        # Shot performance chart data
        try:
            shot_types = ["Draw", "Drive", "Weight"]
            accuracies = []
            for shot_type in shot_types:
                try:
                    accuracy = await crud_practice.get_average_accuracy(
                        db,
                        shot_type=shot_type
                    )
                    accuracies.append(accuracy or 0)
                except Exception as e:
                    logger.error(f"Error fetching accuracy for shot type {shot_type}: {e}")
                    accuracies.append(0)
        except Exception as e:
            logger.error(f"Error generating shot performance chart data: {e}")
            shot_types = ["Draw", "Drive", "Weight"]  # Reset to defaults
            accuracies = [0, 0, 0]  # Reset to defaults

        # Recent activities
        try:
            recent_activities = await crud_practice.get_recent_activities(db, limit=5)
        except Exception as e:
            logger.error(f"Error fetching recent activities: {e}")
            recent_activities = []
    
    except Exception as e:
        # Catch-all exception handler to ensure the dashboard always renders
        logger.error(f"Critical error in admin dashboard: {e}")
        # We already have default values set at the beginning
    
    # Create the chart data dictionary with our gathered data
    chart_data = {
        "user_growth": {
            "labels": months,
            "data": user_counts
        },
        "shot_performance": {
            "labels": shot_types,
            "data": accuracies
        }
    }
    
    # Prepare context with all data (defaults or actual data)
    context = get_admin_context(request)
    context["stats"] = stats
    context["chart_data"] = chart_data
    context["recent_activities"] = recent_activities
    
    # Safely render the template
    try:
        return templates.TemplateResponse("admin/dashboard.html", context)
    except Exception as e:
        logger.error(f"Error rendering admin dashboard template: {e}")
        return HTMLResponse(content="<h1>Admin Dashboard Error</h1><p>There was an error rendering the dashboard. Please check the logs.</p>")
