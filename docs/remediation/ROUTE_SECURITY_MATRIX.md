# Route Security Matrix — Healing Space UK

_Auto-generated from `api.py` by `scripts/gen_route_matrix.py`. Heuristic — the authN/role/
patient-rel columns are detected by scanning each handler body and REQUIRE manual confirmation
during the per-domain refactor (spec §4). Regenerate after each refactor phase._

## IMPORTANT — how enforcement actually works (verified, not per-decorator)

- **CSRF is enforced GLOBALLY** via `@app.before_request csrf_protect()` (api.py:2414), not per
  route. The `CSRF` column below only marks the per-route `@CSRFProtection` decorator and is NOT
  the source of truth. **However the global validator is BROKEN**: `validate_csrf_token()`
  (api.py:~2379) accepts ANY 64-char alphanumeric string and is fully bypassed when `TESTING=1`.
  The token is not session-bound. See SECURITY_FINDINGS SEC-001. Treat ALL state-changing routes
  as effectively CSRF-unprotected until SEC-001 is fixed.
- **Rate limiting**: a global Flask-Limiter default (`200/day, 50/hour`, `storage_uri=memory://`)
  applies to all routes; a second custom in-memory `RateLimiter` guards 12 sensitive endpoints via
  `@check_rate_limit`. Neither is distributed (SEC-003). The `rate` column marks only the custom one.
- **AuthN/role/patient-rel** are enforced INLINE inside handlers (`get_authenticated_username()`,
  `SELECT role FROM users`, `verify_clinician_patient_relationship()`), never via decorators — so
  coverage cannot be guaranteed by inspection and must be centralised (spec §7).

- Total routes parsed: **380**
- State-changing (POST/PUT/PATCH/DELETE): **212**
- State-changing WITHOUT CSRF decorator: **199**
- State-changing WITHOUT detectable authN: **67**
- Routes WITHOUT rate limiting: **374** of 380
- Clinician/patient routes WITHOUT patient-relationship check: **47**

## State-changing routes missing CSRF (HIGH PRIORITY)

| Line | Method | Path | Func | authN | role |
|---|---|---|---|---|---|
| 752 | POST | `/api/cbt/goals` | create_goal | Y | - |
| 817 | PUT | `/api/cbt/goals/<int:entry_id>` | update_goal | Y | - |
| 844 | DELETE | `/api/cbt/goals/<int:entry_id>` | delete_goal | Y | - |
| 867 | POST | `/api/cbt/goals/<int:goal_id>/milestone` | create_goal_milestone | Y | - |
| 906 | POST | `/api/cbt/goals/<int:goal_id>/checkin` | create_goal_checkin | Y | - |
| 962 | POST | `/api/cbt/values` | create_value | Y | - |
| 1027 | PUT | `/api/cbt/values/<int:entry_id>` | update_value | Y | - |
| 1054 | DELETE | `/api/cbt/values/<int:entry_id>` | delete_value | Y | - |
| 1094 | POST | `/api/cbt/self-compassion` | create_self_compassion | Y | - |
| 1155 | PUT | `/api/cbt/self-compassion/<int:entry_id>` | update_self_compassion | Y | - |
| 1182 | DELETE | `/api/cbt/self-compassion/<int:entry_id>` | delete_self_compassion | Y | - |
| 1222 | POST | `/api/cbt/coping-card` | create_coping_card | Y | - |
| 1287 | PUT | `/api/cbt/coping-card/<int:entry_id>` | update_coping_card | Y | - |
| 1314 | DELETE | `/api/cbt/coping-card/<int:entry_id>` | delete_coping_card | Y | - |
| 1354 | POST | `/api/cbt/problem-solving` | create_problem_solving | Y | - |
| 1419 | PUT | `/api/cbt/problem-solving/<int:entry_id>` | update_problem_solving | Y | - |
| 1446 | DELETE | `/api/cbt/problem-solving/<int:entry_id>` | delete_problem_solving | Y | - |
| 1486 | POST | `/api/cbt/exposure` | create_exposure_hierarchy | Y | - |
| 1549 | PUT | `/api/cbt/exposure/<int:entry_id>` | update_exposure_hierarchy | Y | - |
| 1576 | DELETE | `/api/cbt/exposure/<int:entry_id>` | delete_exposure_hierarchy | Y | - |
| 1599 | POST | `/api/cbt/exposure/<int:exposure_id>/attempt` | create_exposure_attempt | Y | - |
| 1659 | POST | `/api/cbt/core-belief` | create_core_belief | Y | - |
| 1725 | PUT | `/api/cbt/core-belief/<int:entry_id>` | update_core_belief | Y | - |
| 1753 | DELETE | `/api/cbt/core-belief/<int:entry_id>` | delete_core_belief | Y | - |
| 1793 | POST | `/api/cbt/sleep` | create_sleep_diary | Y | - |
| 1862 | PUT | `/api/cbt/sleep/<int:entry_id>` | update_sleep_diary | Y | - |
| 1890 | DELETE | `/api/cbt/sleep/<int:entry_id>` | delete_sleep_diary | Y | - |
| 1930 | POST | `/api/cbt/relaxation` | create_relaxation_technique | Y | - |
| 1993 | PUT | `/api/cbt/relaxation/<int:entry_id>` | update_relaxation_technique | Y | - |
| 2021 | DELETE | `/api/cbt/relaxation/<int:entry_id>` | delete_relaxation_technique | Y | - |
| 6635 | POST | `/api/cbt/breathing` | create_breathing_exercise | Y | - |
| 6699 | PUT | `/api/cbt/breathing/<int:entry_id>` | update_breathing_exercise | Y | - |
| 6727 | DELETE | `/api/cbt/breathing/<int:entry_id>` | delete_breathing_exercise | Y | - |
| 6967 | POST | `/api/admin/wipe-database` | admin_wipe_database | - | - |
| 7035 | POST | `/api/auth/send-verification` | send_verification | - | - |
| 7085 | POST | `/api/auth/verify-code` | verify_code | - | - |
| 7132 | POST | `/api/auth/register` | register | - | Y |
| 7290 | POST | `/api/auth/login` | login | Y | Y |
| 7413 | POST | `/api/auth/logout` | logout | Y | - |
| 7427 | POST | `/api/auth/change-password` | change_password | Y | - |
| 7542 | POST | `/api/validate-session` | validate_session | - | - |
| 7582 | POST | `/api/auth/forgot-password` | forgot_password | - | - |
| 7837 | POST | `/api/auth/confirm-reset` | confirm_password_reset | - | - |
| 8018 | POST | `/api/auth/clinician/register` | clinician_register | - | - |
| 8115 | POST | `/api/auth/developer/register` | developer_register | - | Y |
| 8160 | POST | `/api/auth/disclaimer/accept` | accept_disclaimer | - | - |
| 8183 | POST | `/api/developer/terminal/execute` | execute_terminal | - | Y |
| 8345 | POST | `/api/developer/ai/chat` | developer_ai_chat | - | Y |
| 8428 | POST | `/api/developer/messages/send` | send_dev_message | - | Y |
| 8596 | POST | `/api/developer/messages/reply` | reply_dev_message | - | - |
| 8674 | POST | `/api/dev/updates` | post_app_update | Y | Y |
| 8723 | POST | `/api/dev/jobs` | create_dev_job | - | Y |
| 8753 | PUT | `/api/dev/jobs/<int:job_id>` | update_dev_job | - | Y |
| 8782 | DELETE | `/api/dev/jobs/<int:job_id>` | delete_dev_job | - | Y |
| 8799 | POST | `/api/messages/conversation/<username>/archive` | archive_conversation | Y | - |
| 8949 | POST | `/api/developer/users/delete` | delete_user | - | Y |
| 9090 | POST | `/api/notifications/<int:notification_id>/read` | mark_notification_read | - | - |
| 9105 | DELETE | `/api/notifications/<int:notification_id>` | delete_notification | - | - |
| 9223 | POST | `/api/notifications/clear-read` | clear_read_notifications | - | - |
| 9274 | POST | `/api/approvals/<int:approval_id>/approve` | approve_patient | - | - |
| 9331 | POST | `/api/approvals/<int:approval_id>/reject` | reject_patient | - | - |
| 9632 | POST | `/api/therapy/chat` | therapy_chat | Y | - |
| 10054 | POST | `/api/therapy/export` | export_chat_history | - | - |
| 10198 | POST | `/api/therapy/sessions` | create_chat_session | - | - |
| 10240 | PUT | `/api/therapy/sessions/<int:session_id>` | update_chat_session | - | - |
| 10286 | DELETE | `/api/therapy/sessions/<int:session_id>` | delete_chat_session | - | - |
| 10344 | POST | `/api/therapy/greeting` | get_therapy_greeting | - | - |
| 10398 | POST | `/api/therapy/initialize` | initialize_chat | - | - |
| 10475 | POST | `/api/mood/log` | log_mood | Y | - |
| 10661 | POST | `/api/gratitude/log` | log_gratitude | Y | - |
| 10752 | POST | `/api/cbt/breathing` | log_breathing_exercise | - | - |
| 10827 | POST | `/api/cbt/relaxation` | log_relaxation_session | - | - |
| 10898 | POST | `/api/cbt/sleep-diary` | log_sleep_diary | - | - |
| 10980 | POST | `/api/cbt/core-beliefs` | create_core_belief_alt | - | - |
| 11071 | POST | `/api/cbt/exposure` | create_exposure_item | - | - |
| 11107 | POST | `/api/cbt/exposure/<int:exposure_id>/attempt` | log_exposure_attempt | - | - |
| 11234 | POST | `/api/cbt/coping-cards` | create_coping_card_alt | - | - |
| 11271 | POST | `/api/cbt/coping-cards/<int:card_id>/use` | use_coping_card | - | - |
| 11303 | PUT | `/api/cbt/coping-cards/<int:card_id>` | update_coping_card_alt | - | - |
| 11335 | DELETE | `/api/cbt/coping-cards/<int:card_id>` | delete_coping_card_alt | - | - |
| 11391 | POST | `/api/cbt/self-compassion` | log_self_compassion | - | - |
| 11541 | POST | `/api/cbt/goals/<int:goal_id>/milestone` | add_goal_milestone | - | - |
| 11580 | PUT | `/api/cbt/goals/<int:goal_id>/milestone/<int:milestone_id>` | update_milestone | - | - |
| 11638 | POST | `/api/cbt/goals/<int:goal_id>/checkin` | add_goal_checkin | - | - |
| 11798 | POST | `/api/safety/check` | safety_check | - | - |
| 11871 | POST | `/api/ai/trigger-training` | trigger_background_training | - | Y |
| 11910 | POST | `/api/pet/create` | pet_create | - | - |
| 11984 | POST | `/api/pet/feed` | pet_feed | - | - |
| 12021 | POST | `/api/pet/reward` | pet_reward | Y | - |
| 12124 | POST | `/api/pet/buy` | pet_buy | - | - |
| 12194 | POST | `/api/pet/declutter` | pet_declutter | Y | - |
| 12245 | POST | `/api/pet/adventure` | pet_adventure | - | - |
| 12289 | POST | `/api/pet/check-return` | pet_check_return | Y | - |
| 12404 | POST | `/api/pet/apply-decay` | pet_apply_decay | Y | - |
| 12454 | POST | `/api/cbt/thought-record` | cbt_thought_record | - | - |
| 12520 | POST | `/api/clinical/phq9` | submit_phq9 | Y | - |
| 12628 | POST | `/api/clinical/gad7` | submit_gad7 | Y | - |
| 12916 | POST | `/api/community/post/<int:post_id>/pin` | pin_community_post | - | Y |
| 12948 | POST | `/api/community/post` | create_community_post | - | - |
| 13012 | POST | `/api/community/post/<int:post_id>/react` | react_to_post | - | - |
| 13079 | POST | `/api/community/post/<int:post_id>/like` | like_community_post | - | - |
| 13116 | DELETE | `/api/community/post/<int:post_id>` | delete_community_post | - | - |
| 13155 | POST | `/api/community/post/<int:post_id>/reply` | create_reply | - | - |
| 13202 | DELETE | `/api/community/reply/<int:reply_id>` | delete_reply | - | - |
| 13240 | POST | `/api/community/post/<int:post_id>/report` | report_community_post | - | - |
| 13353 | POST | `/api/safety-plan` | save_safety_plan | - | - |
| 14090 | POST | `/api/professional/ai-summary` | generate_ai_summary | Y | Y |
| 14520 | DELETE | `/api/professional/notes/<int:note_id>` | delete_clinician_note | Y | - |
| 14554 | POST | `/api/professional/export-summary` | export_patient_summary | Y | - |
| 14749 | POST | `/api/admin/reset-users` | reset_all_users | - | - |
| 14834 | POST | `/api/mood/check-reminder` | check_mood_reminder | - | - |
| 14924 | POST | `/api/training/consent` | set_training_consent | - | - |
| 14969 | POST | `/api/training/export` | export_training_data | - | - |
| 15008 | POST | `/api/training/delete` | delete_training_data | - | - |
| 15044 | GET,POST | `/api/appointments` | manage_appointments | Y | - |
| 15248 | DELETE | `/api/appointments/<int:appointment_id>` | cancel_appointment | Y | - |
| 15316 | POST | `/api/appointments/<int:appointment_id>/respond` | respond_to_appointment | Y | - |
| 15380 | POST | `/api/appointments/<int:appointment_id>/attendance` | confirm_appointment_attendance | Y | - |
| 15489 | POST | `/api/clinician/availability` | add_clinician_availability | Y | - |
| 15533 | DELETE | `/api/clinician/availability/<int:avail_id>` | delete_clinician_availability | Y | - |
| 15719 | PATCH | `/api/appointments/<int:appointment_id>` | patch_appointment | Y | - |
| 15770 | GET,PUT | `/api/patient/profile` | patient_profile | Y | Y |
| 15982 | POST | `/api/patient/achievements/check-unlocks` | check_achievement_unlocks | Y | - |
| 16464 | POST | `/api/reports/generate` | generate_clinical_report | - | - |
| 17528 | POST | `/api/safeguarding/concerns` | create_safeguarding_concern | Y | Y |
| 17715 | PATCH | `/api/safeguarding/concerns/<int:concern_id>` | update_safeguarding_concern | Y | Y |
| 17892 | POST | `/api/safeguarding/duty` | set_duty_clinician | Y | Y |
| 17953 | DELETE | `/api/safeguarding/duty/<int:duty_id>` | delete_duty_assignment | Y | Y |
| 18520 | POST | `/api/feedback` | submit_feedback | Y | Y |
| 18609 | POST | `/api/daily-tasks/complete` | complete_daily_task | Y | - |
| 18828 | POST | `/api/cbt-tools/save` | save_cbt_tool_entry | Y | - |
| 19014 | POST | `/api/messages/send` | send_message | Y | - |
| 19219 | PATCH | `/api/messages/<int:message_id>/read` | mark_message_read | Y | - |
| 19380 | PUT | `/api/feedback/<int:feedback_id>/status` | update_feedback_status | Y | Y |
| 19453 | DELETE | `/api/messages/<int:message_id>` | delete_message | Y | - |
| 19489 | POST | `/api/messages/<int:message_id>/reply` | reply_to_message | Y | - |
| 19552 | POST | `/api/messages/templates` | create_message_template | Y | - |
| 19640 | PUT | `/api/messages/templates/<int:template_id>` | update_message_template | Y | - |
| 19687 | DELETE | `/api/messages/templates/<int:template_id>` | delete_message_template | Y | - |
| 19724 | POST | `/api/messages/templates/<int:template_id>/use` | use_message_template | Y | - |
| 19777 | POST | `/api/messages/group/create` | create_group_conversation | Y | - |
| 19829 | POST | `/api/messages/group/<int:conversation_id>/send` | send_group_message | Y | - |
| 19878 | POST | `/api/messages/group/<int:conversation_id>/members` | add_group_member | Y | - |
| 19962 | POST | `/api/messages/scheduled` | schedule_message | Y | - |
| 20048 | PATCH | `/api/messages/scheduled/<int:message_id>` | update_scheduled_message | Y | - |
| 20094 | DELETE | `/api/messages/scheduled/<int:message_id>` | cancel_scheduled_message | Y | - |
| 20133 | POST | `/api/messages/block/<username_to_block>` | block_user | Y | - |
| 20180 | DELETE | `/api/messages/block/<username_to_unblock>` | unblock_user | Y | - |
| 20251 | POST | `/api/admin/messages/broadcast` | broadcast_message_admin | Y | Y |
| 20307 | POST | `/api/clinician/messages/broadcast` | broadcast_message_clinician | Y | Y |
| 20415 | PUT | `/api/messages/notifications/settings` | update_notification_settings | Y | - |
| 20585 | POST | `/api/messages/archive/<int:message_id>` | archive_message | Y | - |
| 20626 | DELETE | `/api/messages/archive/<int:message_id>` | unarchive_message | Y | - |
| 20760 | POST | `/api/developer/tests/save` | save_test_results | Y | Y |
| 20795 | POST | `/api/developer/tests/run` | run_tests | Y | Y |
| 20911 | POST | `/api/developer/performance/run` | run_performance_tests | Y | Y |
| 21081 | POST | `/api/developer/test-data/generate` | generate_test_data | Y | Y |
| 21315 | POST | `/api/developer/tests/verbose` | run_verbose_tests | Y | Y |
| 21551 | POST | `/api/wellness/log` | create_wellness_log | Y | - |
| 21798 | POST | `/api/user/medications` | add_user_medication | Y | - |
| 21842 | PUT | `/api/user/medications/<int:med_id>` | update_user_medication | Y | - |
| 21885 | DELETE | `/api/user/medications/<int:med_id>` | delete_user_medication | Y | - |
| 21909 | POST | `/api/user/medications/<int:med_id>/log` | log_medication_dose | Y | - |
| 22160 | POST | `/api/user/quests/accept` | accept_quest | Y | - |
| 22214 | POST | `/api/user/quests/<int:quest_id>/abandon` | abandon_quest | Y | - |
| 22281 | POST | `/api/clinician/patient/<patient_username>/quests/assign` | clinician_assign_quest | Y | Y |
| 22341 | POST | `/api/user/spell/cast` | record_spell_cast | Y | - |
| 22485 | POST | `/api/clinician/waiting-list` | add_to_waiting_list | Y | Y |
| 22537 | PUT | `/api/clinician/waiting-list/<int:entry_id>` | update_waiting_list_entry | Y | - |
| 22571 | POST | `/api/clinician/waiting-list/<int:entry_id>/convert` | convert_waiting_to_patient | Y | - |
| 22601 | DELETE | `/api/clinician/waiting-list/<int:entry_id>` | remove_from_waiting_list | Y | - |
| 22893 | POST | `/api/clinician/patient/<patient_username>/milestone-message` | send_milestone_message | Y | Y |
| 23350 | POST | `/api/activity/log` | log_activity_endpoint | Y | - |
| 23448 | POST | `/api/activity/consent` | set_activity_consent | Y | - |
| 23492 | POST | `/api/ai/memory/update` | update_ai_memory_endpoint | Y | - |
| 23567 | POST | `/api/ai/patterns/detect` | detect_patterns_endpoint | - | Y |
| 23669 | POST | `/api/clinician/summaries/generate` | generate_clinician_summaries_endpoint | - | - |
| 23926 | POST | `/api/clinician/approve-patient` | clinician_approve_patient | Y | Y |
| 24026 | POST | `/api/clinician/reject-patient` | clinician_reject_patient | Y | Y |
| 25086 | POST | `/api/clinician/message` | send_clinician_message | Y | Y |
| 25177 | POST | `/api/wins/log` | log_win | Y | - |
| 25512 | POST | `/api/c-ssrs/start` | start_c_ssrs_assessment | Y | - |
| 25547 | POST | `/api/c-ssrs/submit` | submit_c_ssrs_assessment | Y | - |
| 25824 | POST | `/api/c-ssrs/<int:assessment_id>/clinician-response` | clinician_c_ssrs_response | Y | - |
| 25875 | POST | `/api/c-ssrs/<int:assessment_id>/safety-plan` | submit_safety_plan | Y | - |
| 25992 | POST | `/api/crisis/detect` | detect_crisis_risk | Y | - |
| 26154 | POST | `/api/crisis/alerts/<int:alert_id>/acknowledge` | acknowledge_crisis_alert | Y | - |
| 26221 | POST | `/api/crisis/alerts/<int:alert_id>/resolve` | resolve_crisis_alert | Y | - |
| 26279 | GET,POST,PUT,DELETE | `/api/crisis/contacts` | manage_crisis_contacts | Y | - |
| 26597 | POST | `/api/clinician/session-notes` | create_session_note | Y | Y |
| 26646 | PUT | `/api/clinician/session-notes/<int:note_id>` | update_session_note | Y | Y |
| 26708 | POST | `/api/clinician/session-notes/<int:note_id>/sign-off` | sign_off_session_note | Y | Y |
| 26825 | POST | `/api/clinician/treatment-plan` | create_treatment_plan | Y | Y |
| 26881 | PUT | `/api/clinician/treatment-plan/<int:plan_id>` | update_treatment_plan | Y | Y |
| 26939 | POST | `/api/clinician/treatment-plan/<int:plan_id>/sign` | clinician_sign_treatment_plan | Y | Y |
| 26971 | POST | `/api/patient/treatment-plan/sign` | patient_sign_treatment_plan | Y | Y |
| 27007 | POST | `/api/patient/treatment-plan/decline` | patient_decline_treatment_plan | Y | Y |
| 27084 | POST | `/api/patient/outcome-measure` | patient_submit_outcome_measure | Y | Y |
| 27161 | POST | `/api/clinician/outcome-measure` | clinician_record_outcome_measure | Y | Y |

## State-changing routes with NO detectable authentication (CRITICAL to review)

| Line | Method | Path | Func | csrf |
|---|---|---|---|---|
| 6967 | POST | `/api/admin/wipe-database` | admin_wipe_database | - |
| 7035 | POST | `/api/auth/send-verification` | send_verification | - |
| 7085 | POST | `/api/auth/verify-code` | verify_code | - |
| 7132 | POST | `/api/auth/register` | register | - |
| 7542 | POST | `/api/validate-session` | validate_session | - |
| 7582 | POST | `/api/auth/forgot-password` | forgot_password | - |
| 7837 | POST | `/api/auth/confirm-reset` | confirm_password_reset | - |
| 8018 | POST | `/api/auth/clinician/register` | clinician_register | - |
| 8115 | POST | `/api/auth/developer/register` | developer_register | - |
| 8160 | POST | `/api/auth/disclaimer/accept` | accept_disclaimer | - |
| 8183 | POST | `/api/developer/terminal/execute` | execute_terminal | - |
| 8345 | POST | `/api/developer/ai/chat` | developer_ai_chat | - |
| 8428 | POST | `/api/developer/messages/send` | send_dev_message | - |
| 8596 | POST | `/api/developer/messages/reply` | reply_dev_message | - |
| 8723 | POST | `/api/dev/jobs` | create_dev_job | - |
| 8753 | PUT | `/api/dev/jobs/<int:job_id>` | update_dev_job | - |
| 8782 | DELETE | `/api/dev/jobs/<int:job_id>` | delete_dev_job | - |
| 8949 | POST | `/api/developer/users/delete` | delete_user | - |
| 9090 | POST | `/api/notifications/<int:notification_id>/read` | mark_notification_read | - |
| 9105 | DELETE | `/api/notifications/<int:notification_id>` | delete_notification | - |
| 9223 | POST | `/api/notifications/clear-read` | clear_read_notifications | - |
| 9274 | POST | `/api/approvals/<int:approval_id>/approve` | approve_patient | - |
| 9331 | POST | `/api/approvals/<int:approval_id>/reject` | reject_patient | - |
| 10054 | POST | `/api/therapy/export` | export_chat_history | - |
| 10198 | POST | `/api/therapy/sessions` | create_chat_session | - |
| 10240 | PUT | `/api/therapy/sessions/<int:session_id>` | update_chat_session | - |
| 10286 | DELETE | `/api/therapy/sessions/<int:session_id>` | delete_chat_session | - |
| 10344 | POST | `/api/therapy/greeting` | get_therapy_greeting | - |
| 10398 | POST | `/api/therapy/initialize` | initialize_chat | - |
| 10752 | POST | `/api/cbt/breathing` | log_breathing_exercise | - |
| 10827 | POST | `/api/cbt/relaxation` | log_relaxation_session | - |
| 10898 | POST | `/api/cbt/sleep-diary` | log_sleep_diary | - |
| 10980 | POST | `/api/cbt/core-beliefs` | create_core_belief_alt | - |
| 11071 | POST | `/api/cbt/exposure` | create_exposure_item | - |
| 11107 | POST | `/api/cbt/exposure/<int:exposure_id>/attempt` | log_exposure_attempt | - |
| 11234 | POST | `/api/cbt/coping-cards` | create_coping_card_alt | - |
| 11271 | POST | `/api/cbt/coping-cards/<int:card_id>/use` | use_coping_card | - |
| 11303 | PUT | `/api/cbt/coping-cards/<int:card_id>` | update_coping_card_alt | - |
| 11335 | DELETE | `/api/cbt/coping-cards/<int:card_id>` | delete_coping_card_alt | - |
| 11391 | POST | `/api/cbt/self-compassion` | log_self_compassion | - |
| 11541 | POST | `/api/cbt/goals/<int:goal_id>/milestone` | add_goal_milestone | - |
| 11580 | PUT | `/api/cbt/goals/<int:goal_id>/milestone/<int:milestone_id>` | update_milestone | - |
| 11638 | POST | `/api/cbt/goals/<int:goal_id>/checkin` | add_goal_checkin | - |
| 11798 | POST | `/api/safety/check` | safety_check | - |
| 11871 | POST | `/api/ai/trigger-training` | trigger_background_training | - |
| 11910 | POST | `/api/pet/create` | pet_create | - |
| 11984 | POST | `/api/pet/feed` | pet_feed | - |
| 12124 | POST | `/api/pet/buy` | pet_buy | - |
| 12245 | POST | `/api/pet/adventure` | pet_adventure | - |
| 12454 | POST | `/api/cbt/thought-record` | cbt_thought_record | - |
| 12916 | POST | `/api/community/post/<int:post_id>/pin` | pin_community_post | - |
| 12948 | POST | `/api/community/post` | create_community_post | - |
| 13012 | POST | `/api/community/post/<int:post_id>/react` | react_to_post | - |
| 13079 | POST | `/api/community/post/<int:post_id>/like` | like_community_post | - |
| 13116 | DELETE | `/api/community/post/<int:post_id>` | delete_community_post | - |
| 13155 | POST | `/api/community/post/<int:post_id>/reply` | create_reply | - |
| 13202 | DELETE | `/api/community/reply/<int:reply_id>` | delete_reply | - |
| 13240 | POST | `/api/community/post/<int:post_id>/report` | report_community_post | - |
| 13353 | POST | `/api/safety-plan` | save_safety_plan | - |
| 14749 | POST | `/api/admin/reset-users` | reset_all_users | - |
| 14834 | POST | `/api/mood/check-reminder` | check_mood_reminder | - |
| 14924 | POST | `/api/training/consent` | set_training_consent | - |
| 14969 | POST | `/api/training/export` | export_training_data | - |
| 15008 | POST | `/api/training/delete` | delete_training_data | - |
| 16464 | POST | `/api/reports/generate` | generate_clinical_report | - |
| 23567 | POST | `/api/ai/patterns/detect` | detect_patterns_endpoint | - |
| 23669 | POST | `/api/clinician/summaries/generate` | generate_clinician_summaries_endpoint | - |

## FULL MATRIX

| Line | Method | Path | authN | role | patient-rel | CSRF | rate |
|---|---|---|---|---|---|---|---|
| 752 | POST | `/api/cbt/goals` | Y | - | - | - | - |
| 782 | GET | `/api/cbt/goals` | Y | - | - | - | - |
| 798 | GET | `/api/cbt/goals/<int:entry_id>` | Y | - | - | - | - |
| 817 | PUT | `/api/cbt/goals/<int:entry_id>` | Y | - | - | - | - |
| 844 | DELETE | `/api/cbt/goals/<int:entry_id>` | Y | - | - | - | - |
| 867 | POST | `/api/cbt/goals/<int:goal_id>/milestone` | Y | - | - | - | - |
| 889 | GET | `/api/cbt/goals/<int:goal_id>/milestone` | Y | - | - | - | - |
| 906 | POST | `/api/cbt/goals/<int:goal_id>/checkin` | Y | - | - | - | - |
| 928 | GET | `/api/cbt/goals/<int:goal_id>/checkin` | Y | - | - | - | - |
| 962 | POST | `/api/cbt/values` | Y | - | - | - | - |
| 992 | GET | `/api/cbt/values` | Y | - | - | - | - |
| 1008 | GET | `/api/cbt/values/<int:entry_id>` | Y | - | - | - | - |
| 1027 | PUT | `/api/cbt/values/<int:entry_id>` | Y | - | - | - | - |
| 1054 | DELETE | `/api/cbt/values/<int:entry_id>` | Y | - | - | - | - |
| 1094 | POST | `/api/cbt/self-compassion` | Y | - | - | - | - |
| 1120 | GET | `/api/cbt/self-compassion` | Y | - | - | - | - |
| 1136 | GET | `/api/cbt/self-compassion/<int:entry_id>` | Y | - | - | - | - |
| 1155 | PUT | `/api/cbt/self-compassion/<int:entry_id>` | Y | - | - | - | - |
| 1182 | DELETE | `/api/cbt/self-compassion/<int:entry_id>` | Y | - | - | - | - |
| 1222 | POST | `/api/cbt/coping-card` | Y | - | - | - | - |
| 1252 | GET | `/api/cbt/coping-card` | Y | - | - | - | - |
| 1268 | GET | `/api/cbt/coping-card/<int:entry_id>` | Y | - | - | - | - |
| 1287 | PUT | `/api/cbt/coping-card/<int:entry_id>` | Y | - | - | - | - |
| 1314 | DELETE | `/api/cbt/coping-card/<int:entry_id>` | Y | - | - | - | - |
| 1354 | POST | `/api/cbt/problem-solving` | Y | - | - | - | - |
| 1384 | GET | `/api/cbt/problem-solving` | Y | - | - | - | - |
| 1400 | GET | `/api/cbt/problem-solving/<int:entry_id>` | Y | - | - | - | - |
| 1419 | PUT | `/api/cbt/problem-solving/<int:entry_id>` | Y | - | - | - | - |
| 1446 | DELETE | `/api/cbt/problem-solving/<int:entry_id>` | Y | - | - | - | - |
| 1486 | POST | `/api/cbt/exposure` | Y | - | - | - | - |
| 1514 | GET | `/api/cbt/exposure` | Y | - | - | - | - |
| 1530 | GET | `/api/cbt/exposure/<int:entry_id>` | Y | - | - | - | - |
| 1549 | PUT | `/api/cbt/exposure/<int:entry_id>` | Y | - | - | - | - |
| 1576 | DELETE | `/api/cbt/exposure/<int:entry_id>` | Y | - | - | - | - |
| 1599 | POST | `/api/cbt/exposure/<int:exposure_id>/attempt` | Y | - | - | - | - |
| 1624 | GET | `/api/cbt/exposure/<int:exposure_id>/attempt` | Y | - | - | - | - |
| 1659 | POST | `/api/cbt/core-belief` | Y | - | - | - | - |
| 1690 | GET | `/api/cbt/core-belief` | Y | - | - | - | - |
| 1706 | GET | `/api/cbt/core-belief/<int:entry_id>` | Y | - | - | - | - |
| 1725 | PUT | `/api/cbt/core-belief/<int:entry_id>` | Y | - | - | - | - |
| 1753 | DELETE | `/api/cbt/core-belief/<int:entry_id>` | Y | - | - | - | - |
| 1793 | POST | `/api/cbt/sleep` | Y | - | - | - | - |
| 1827 | GET | `/api/cbt/sleep` | Y | - | - | - | - |
| 1843 | GET | `/api/cbt/sleep/<int:entry_id>` | Y | - | - | - | - |
| 1862 | PUT | `/api/cbt/sleep/<int:entry_id>` | Y | - | - | - | - |
| 1890 | DELETE | `/api/cbt/sleep/<int:entry_id>` | Y | - | - | - | - |
| 1930 | POST | `/api/cbt/relaxation` | Y | - | - | - | - |
| 1958 | GET | `/api/cbt/relaxation` | Y | - | - | - | - |
| 1974 | GET | `/api/cbt/relaxation/<int:entry_id>` | Y | - | - | - | - |
| 1993 | PUT | `/api/cbt/relaxation/<int:entry_id>` | Y | - | - | - | - |
| 2021 | DELETE | `/api/cbt/relaxation/<int:entry_id>` | Y | - | - | - | - |
| 2468 | GET | `/api/csrf-token` | - | - | - | - | - |
| 2478 | GET | `/api/auth/status` | Y | - | - | - | - |
| 6635 | POST | `/api/cbt/breathing` | Y | - | - | - | - |
| 6664 | GET | `/api/cbt/breathing` | Y | - | - | - | - |
| 6680 | GET | `/api/cbt/breathing/<int:entry_id>` | Y | - | - | - | - |
| 6699 | PUT | `/api/cbt/breathing/<int:entry_id>` | Y | - | - | - | - |
| 6727 | DELETE | `/api/cbt/breathing/<int:entry_id>` | Y | - | - | - | - |
| 6812 | GET | `/favicon.ico` | - | - | - | - | - |
| 6817 | GET | `/` | - | - | - | - | - |
| 6822 | GET | `/login` | - | - | - | - | - |
| 6827 | GET | `/api/admin/wipe` | Y | Y | - | - | - |
| 6841 | GET | `/api/developer/dashboard` | Y | Y | - | - | - |
| 6863 | GET | `/api/debug/analytics/<clinician>` | Y | Y | - | - | - |
| 6952 | GET | `/diagnostic` | - | - | - | - | - |
| 6957 | GET | `/api/health` | - | - | - | - | - |
| 6967 | POST | `/api/admin/wipe-database` | - | - | - | - | - |
| 7035 | POST | `/api/auth/send-verification` | - | - | - | - | - |
| 7085 | POST | `/api/auth/verify-code` | - | - | - | - | Y |
| 7132 | POST | `/api/auth/register` | - | Y | - | - | Y |
| 7290 | POST | `/api/auth/login` | Y | Y | - | - | Y |
| 7413 | POST | `/api/auth/logout` | Y | - | - | - | - |
| 7427 | POST | `/api/auth/change-password` | Y | - | - | - | - |
| 7542 | POST | `/api/validate-session` | - | - | - | - | - |
| 7582 | POST | `/api/auth/forgot-password` | - | - | - | - | Y |
| 7837 | POST | `/api/auth/confirm-reset` | - | - | - | - | - |
| 8018 | POST | `/api/auth/clinician/register` | - | - | - | - | - |
| 8115 | POST | `/api/auth/developer/register` | - | Y | - | - | - |
| 8160 | POST | `/api/auth/disclaimer/accept` | - | - | - | - | - |
| 8183 | POST | `/api/developer/terminal/execute` | - | Y | - | - | - |
| 8345 | POST | `/api/developer/ai/chat` | - | Y | - | - | - |
| 8428 | POST | `/api/developer/messages/send` | - | Y | - | - | - |
| 8545 | GET | `/api/developer/messages/list` | - | Y | - | - | - |
| 8596 | POST | `/api/developer/messages/reply` | - | - | - | - | - |
| 8640 | GET | `/api/dev/updates` | - | - | - | - | - |
| 8674 | POST | `/api/dev/updates` | Y | Y | - | - | - |
| 8701 | GET | `/api/dev/jobs` | - | Y | - | - | - |
| 8723 | POST | `/api/dev/jobs` | - | Y | - | - | - |
| 8753 | PUT | `/api/dev/jobs/<int:job_id>` | - | Y | - | - | - |
| 8782 | DELETE | `/api/dev/jobs/<int:job_id>` | - | Y | - | - | - |
| 8799 | POST | `/api/messages/conversation/<username>/archive` | Y | - | - | - | - |
| 8835 | GET | `/api/dev/archived-conversations` | Y | Y | - | - | - |
| 8861 | GET | `/api/developer/stats` | - | Y | - | - | - |
| 8900 | GET | `/api/developer/users/list` | - | Y | - | - | - |
| 8949 | POST | `/api/developer/users/delete` | - | Y | - | - | - |
| 9012 | GET | `/api/clinicians/list` | - | Y | - | - | - |
| 9059 | GET | `/api/notifications` | - | - | - | - | - |
| 9090 | POST | `/api/notifications/<int:notification_id>/read` | - | - | - | - | - |
| 9105 | DELETE | `/api/notifications/<int:notification_id>` | - | - | - | - | - |
| 9120 | GET | `/api/poll` | Y | Y | - | - | - |
| 9223 | POST | `/api/notifications/clear-read` | - | - | - | - | - |
| 9245 | GET | `/api/approvals/pending` | - | - | - | - | - |
| 9274 | POST | `/api/approvals/<int:approval_id>/approve` | - | - | - | - | - |
| 9331 | POST | `/api/approvals/<int:approval_id>/reject` | - | - | - | - | - |
| 9632 | POST | `/api/therapy/chat` | Y | - | - | - | Y |
| 10007 | GET | `/api/therapy/history` | Y | - | - | - | - |
| 10054 | POST | `/api/therapy/export` | - | - | - | - | - |
| 10151 | GET | `/api/therapy/sessions` | - | - | - | - | - |
| 10198 | POST | `/api/therapy/sessions` | - | - | - | - | - |
| 10240 | PUT | `/api/therapy/sessions/<int:session_id>` | - | - | - | - | - |
| 10286 | DELETE | `/api/therapy/sessions/<int:session_id>` | - | - | - | - | - |
| 10344 | POST | `/api/therapy/greeting` | - | - | - | - | - |
| 10398 | POST | `/api/therapy/initialize` | - | - | - | - | - |
| 10475 | POST | `/api/mood/log` | Y | - | - | - | - |
| 10621 | GET | `/api/mood/history` | Y | - | - | - | - |
| 10661 | POST | `/api/gratitude/log` | Y | - | - | - | - |
| 10723 | GET | `/api/cbt/breathing` | - | - | - | - | - |
| 10752 | POST | `/api/cbt/breathing` | - | - | - | - | - |
| 10798 | GET | `/api/cbt/relaxation` | - | - | - | - | - |
| 10827 | POST | `/api/cbt/relaxation` | - | - | - | - | - |
| 10866 | GET | `/api/cbt/sleep-diary` | - | - | - | - | - |
| 10898 | POST | `/api/cbt/sleep-diary` | - | - | - | - | - |
| 10946 | GET | `/api/cbt/core-beliefs` | - | - | - | - | - |
| 10980 | POST | `/api/cbt/core-beliefs` | - | - | - | - | - |
| 11026 | GET | `/api/cbt/exposure` | - | - | - | - | - |
| 11071 | POST | `/api/cbt/exposure` | - | - | - | - | - |
| 11107 | POST | `/api/cbt/exposure/<int:exposure_id>/attempt` | - | - | - | - | - |
| 11163 | GET | `/api/cbt/problem-solving` | - | - | - | - | - |
| 11200 | GET | `/api/cbt/coping-cards` | - | - | - | - | - |
| 11234 | POST | `/api/cbt/coping-cards` | - | - | - | - | - |
| 11271 | POST | `/api/cbt/coping-cards/<int:card_id>/use` | - | - | - | - | - |
| 11303 | PUT | `/api/cbt/coping-cards/<int:card_id>` | - | - | - | - | - |
| 11335 | DELETE | `/api/cbt/coping-cards/<int:card_id>` | - | - | - | - | - |
| 11362 | GET | `/api/cbt/self-compassion` | - | - | - | - | - |
| 11391 | POST | `/api/cbt/self-compassion` | - | - | - | - | - |
| 11432 | GET | `/api/cbt/values` | - | - | - | - | - |
| 11469 | GET | `/api/cbt/goals` | - | - | - | - | - |
| 11541 | POST | `/api/cbt/goals/<int:goal_id>/milestone` | - | - | - | - | - |
| 11580 | PUT | `/api/cbt/goals/<int:goal_id>/milestone/<int:milestone_id>` | - | - | - | - | - |
| 11638 | POST | `/api/cbt/goals/<int:goal_id>/checkin` | - | - | - | - | - |
| 11684 | GET | `/api/cbt/summary` | - | - | - | - | - |
| 11775 | GET | `/api/export/fhir` | - | - | - | - | - |
| 11798 | POST | `/api/safety/check` | - | - | - | - | - |
| 11840 | GET | `/api/pet/status` | - | - | - | - | - |
| 11871 | POST | `/api/ai/trigger-training` | - | Y | - | - | - |
| 11910 | POST | `/api/pet/create` | - | - | - | - | - |
| 11984 | POST | `/api/pet/feed` | - | - | - | - | - |
| 12021 | POST | `/api/pet/reward` | Y | - | - | - | - |
| 12109 | GET | `/api/pet/shop` | - | - | - | - | - |
| 12124 | POST | `/api/pet/buy` | - | - | - | - | - |
| 12194 | POST | `/api/pet/declutter` | Y | - | - | - | - |
| 12245 | POST | `/api/pet/adventure` | - | - | - | - | - |
| 12289 | POST | `/api/pet/check-return` | Y | - | - | - | - |
| 12374 | GET | `/api/pet/inventory` | Y | - | - | - | - |
| 12404 | POST | `/api/pet/apply-decay` | Y | - | - | - | - |
| 12454 | POST | `/api/cbt/thought-record` | - | - | - | - | - |
| 12492 | GET | `/api/cbt/records` | - | - | - | - | - |
| 12520 | POST | `/api/clinical/phq9` | Y | - | - | - | - |
| 12628 | POST | `/api/clinical/gad7` | Y | - | - | - | - |
| 12733 | GET | `/api/community/posts` | - | - | - | - | - |
| 12838 | GET | `/api/community/channels` | - | - | - | - | - |
| 12916 | POST | `/api/community/post/<int:post_id>/pin` | - | Y | - | - | - |
| 12948 | POST | `/api/community/post` | - | - | - | - | - |
| 13012 | POST | `/api/community/post/<int:post_id>/react` | - | - | - | - | - |
| 13079 | POST | `/api/community/post/<int:post_id>/like` | - | - | - | - | - |
| 13116 | DELETE | `/api/community/post/<int:post_id>` | - | - | - | - | - |
| 13155 | POST | `/api/community/post/<int:post_id>/reply` | - | - | - | - | - |
| 13202 | DELETE | `/api/community/reply/<int:reply_id>` | - | - | - | - | - |
| 13240 | POST | `/api/community/post/<int:post_id>/report` | - | - | - | - | - |
| 13301 | GET | `/api/community/post/<int:post_id>/replies` | - | - | - | - | - |
| 13325 | GET | `/api/safety-plan` | - | - | - | - | - |
| 13353 | POST | `/api/safety-plan` | - | - | - | - | - |
| 13392 | GET | `/api/export/csv` | - | - | - | - | - |
| 13455 | GET | `/api/export/pdf` | - | - | - | - | - |
| 13561 | GET | `/api/insights` | Y | Y | - | - | - |
| 13767 | GET | `/api/professional/patients` | Y | Y | - | - | - |
| 13864 | GET | `/api/professional/patient/<username>` | Y | Y | Y | - | - |
| 14090 | POST | `/api/professional/ai-summary` | Y | Y | - | - | - |
| 14436 | POST | `/api/professional/notes` | Y | - | Y | Y | - |
| 14485 | GET | `/api/professional/notes/<patient_username>` | Y | - | Y | - | - |
| 14520 | DELETE | `/api/professional/notes/<int:note_id>` | Y | - | - | - | - |
| 14554 | POST | `/api/professional/export-summary` | Y | - | - | - | - |
| 14749 | POST | `/api/admin/reset-users` | - | - | - | - | - |
| 14834 | POST | `/api/mood/check-reminder` | - | - | - | - | - |
| 14890 | GET | `/api/mood/check-today` | - | - | - | - | - |
| 14924 | POST | `/api/training/consent` | - | - | - | - | - |
| 14952 | GET | `/api/training/consent/status` | - | - | - | - | - |
| 14969 | POST | `/api/training/export` | - | - | - | - | - |
| 15008 | POST | `/api/training/delete` | - | - | - | - | - |
| 15028 | GET | `/api/training/stats` | - | - | - | - | - |
| 15044 | GET,POST | `/api/appointments` | Y | - | - | - | - |
| 15248 | DELETE | `/api/appointments/<int:appointment_id>` | Y | - | - | - | - |
| 15316 | POST | `/api/appointments/<int:appointment_id>/respond` | Y | - | - | - | - |
| 15380 | POST | `/api/appointments/<int:appointment_id>/attendance` | Y | - | - | - | - |
| 15448 | GET | `/api/clinician/availability` | Y | - | - | - | - |
| 15489 | POST | `/api/clinician/availability` | Y | - | - | - | - |
| 15533 | DELETE | `/api/clinician/availability/<int:avail_id>` | Y | - | - | - | - |
| 15560 | GET | `/api/appointments/available-slots` | Y | - | - | - | - |
| 15669 | GET | `/api/appointments/dna-report` | Y | - | - | - | - |
| 15719 | PATCH | `/api/appointments/<int:appointment_id>` | Y | - | - | - | - |
| 15770 | GET,PUT | `/api/patient/profile` | Y | Y | - | - | - |
| 15862 | GET | `/api/patient/progress/mood` | Y | - | - | - | - |
| 15941 | GET | `/api/patient/achievements` | Y | - | - | - | - |
| 15982 | POST | `/api/patient/achievements/check-unlocks` | Y | - | - | - | - |
| 16056 | GET | `/api/patient/homework` | Y | - | - | - | - |
| 16098 | GET | `/api/analytics/dashboard` | - | - | - | - | - |
| 16249 | GET | `/api/analytics/active-patients` | - | - | - | - | - |
| 16329 | GET | `/api/analytics/patient/<username>` | Y | Y | Y | - | - |
| 16464 | POST | `/api/reports/generate` | - | - | - | - | - |
| 16641 | GET | `/api/patients/search` | - | - | - | - | - |
| 16711 | GET | `/api/risk/score/<username>` | Y | Y | - | - | - |
| 16761 | GET | `/api/risk/history/<username>` | Y | Y | - | - | - |
| 16825 | GET | `/api/risk/alerts` | Y | Y | - | - | - |
| 16906 | POST | `/api/risk/alert` | Y | Y | - | Y | - |
| 16980 | PATCH | `/api/risk/alert/<int:alert_id>/acknowledge` | Y | Y | - | Y | - |
| 17023 | PATCH | `/api/risk/alert/<int:alert_id>/resolve` | Y | Y | - | Y | - |
| 17077 | GET | `/api/risk/keywords` | Y | Y | - | - | - |
| 17117 | POST | `/api/risk/keywords` | Y | Y | - | Y | - |
| 17174 | GET | `/api/risk/dashboard` | Y | Y | - | - | - |
| 17346 | GET | `/api/risk/predictive/<patient_username>` | Y | Y | - | - | - |
| 17389 | PATCH | `/api/risk/predictive/<int:flag_id>/dismiss` | Y | Y | - | Y | - |
| 17427 | GET | `/api/safeguarding/stats` | Y | Y | - | - | - |
| 17472 | GET | `/api/safeguarding/concerns` | Y | Y | - | - | - |
| 17528 | POST | `/api/safeguarding/concerns` | Y | Y | - | - | - |
| 17664 | GET | `/api/safeguarding/concerns/<int:concern_id>` | Y | Y | - | - | - |
| 17715 | PATCH | `/api/safeguarding/concerns/<int:concern_id>` | Y | Y | - | - | - |
| 17776 | GET | `/api/safeguarding/patient/<patient_username>` | Y | Y | - | - | - |
| 17824 | GET | `/api/safeguarding/duty` | Y | Y | - | - | - |
| 17892 | POST | `/api/safeguarding/duty` | Y | Y | - | - | - |
| 17953 | DELETE | `/api/safeguarding/duty/<int:duty_id>` | Y | Y | - | - | - |
| 17984 | GET | `/api/safety-plan/<username>` | Y | Y | - | - | - |
| 18045 | PUT | `/api/safety-plan/<username>` | Y | - | - | Y | - |
| 18105 | GET | `/api/safety/check-in/<username>` | Y | - | - | - | - |
| 18176 | GET | `/api/consent/ai-monitoring/<username>` | Y | Y | - | - | - |
| 18215 | POST | `/api/consent/ai-monitoring/<username>` | Y | - | - | Y | - |
| 18245 | DELETE | `/api/consent/ai-monitoring/<username>` | Y | - | - | Y | - |
| 18276 | GET | `/api/risk/report/individual/<username>` | Y | Y | - | - | - |
| 18379 | GET | `/api/risk/report/caseload` | Y | Y | - | - | - |
| 18463 | GET | `/api/home/data` | Y | - | - | - | - |
| 18520 | POST | `/api/feedback` | Y | Y | - | - | - |
| 18579 | GET | `/api/feedback` | Y | - | - | - | - |
| 18609 | POST | `/api/daily-tasks/complete` | Y | - | - | - | - |
| 18729 | GET | `/api/daily-tasks/streak` | Y | - | - | - | - |
| 18803 | GET | `/cbt_tools/components/<path:filename>` | - | - | - | - | - |
| 18828 | POST | `/api/cbt-tools/save` | Y | - | - | - | - |
| 18922 | GET | `/api/cbt-tools/load` | Y | - | - | - | - |
| 18964 | GET | `/api/cbt-tools/history` | Y | - | - | - | - |
| 19014 | POST | `/api/messages/send` | Y | - | - | - | - |
| 19117 | GET | `/api/messages/inbox` | Y | - | - | - | - |
| 19171 | GET | `/api/messages/conversation/<recipient_username>` | Y | - | - | - | - |
| 19219 | PATCH | `/api/messages/<int:message_id>/read` | Y | - | - | - | - |
| 19257 | GET | `/api/messages/search` | Y | - | - | - | - |
| 19297 | GET | `/api/messages/sent` | Y | - | - | - | - |
| 19333 | GET | `/api/feedback/all` | Y | Y | - | - | - |
| 19380 | PUT | `/api/feedback/<int:feedback_id>/status` | Y | Y | - | - | - |
| 19453 | DELETE | `/api/messages/<int:message_id>` | Y | - | - | - | - |
| 19489 | POST | `/api/messages/<int:message_id>/reply` | Y | - | - | - | - |
| 19552 | POST | `/api/messages/templates` | Y | - | - | - | - |
| 19608 | GET | `/api/messages/templates` | Y | - | - | - | - |
| 19640 | PUT | `/api/messages/templates/<int:template_id>` | Y | - | - | - | - |
| 19687 | DELETE | `/api/messages/templates/<int:template_id>` | Y | - | - | - | - |
| 19724 | POST | `/api/messages/templates/<int:template_id>/use` | Y | - | - | - | - |
| 19777 | POST | `/api/messages/group/create` | Y | - | - | - | - |
| 19829 | POST | `/api/messages/group/<int:conversation_id>/send` | Y | - | - | - | - |
| 19878 | POST | `/api/messages/group/<int:conversation_id>/members` | Y | - | - | - | - |
| 19925 | GET | `/api/messages/group/<int:conversation_id>/members` | Y | - | - | - | - |
| 19962 | POST | `/api/messages/scheduled` | Y | - | - | - | - |
| 20016 | GET | `/api/messages/scheduled` | Y | - | - | - | - |
| 20048 | PATCH | `/api/messages/scheduled/<int:message_id>` | Y | - | - | - | - |
| 20094 | DELETE | `/api/messages/scheduled/<int:message_id>` | Y | - | - | - | - |
| 20133 | POST | `/api/messages/block/<username_to_block>` | Y | - | - | - | - |
| 20180 | DELETE | `/api/messages/block/<username_to_unblock>` | Y | - | - | - | - |
| 20217 | GET | `/api/messages/blocked` | Y | - | - | - | - |
| 20251 | POST | `/api/admin/messages/broadcast` | Y | Y | - | - | - |
| 20307 | POST | `/api/clinician/messages/broadcast` | Y | Y | - | - | - |
| 20365 | GET | `/api/messages/notifications/settings` | Y | - | - | - | - |
| 20415 | PUT | `/api/messages/notifications/settings` | Y | - | - | - | - |
| 20487 | GET | `/api/messages/unread-count` | Y | - | - | - | - |
| 20518 | GET | `/api/messages/search-recipients` | Y | Y | - | - | - |
| 20585 | POST | `/api/messages/archive/<int:message_id>` | Y | - | - | - | - |
| 20626 | DELETE | `/api/messages/archive/<int:message_id>` | Y | - | - | - | - |
| 20665 | GET | `/api/admin/messages/analytics` | Y | Y | - | - | - |
| 20705 | GET | `/api/clinician/messages/analytics` | Y | Y | - | - | - |
| 20760 | POST | `/api/developer/tests/save` | Y | Y | - | - | - |
| 20795 | POST | `/api/developer/tests/run` | Y | Y | - | - | - |
| 20867 | GET | `/api/developer/tests/results` | Y | Y | - | - | - |
| 20911 | POST | `/api/developer/performance/run` | Y | Y | - | - | - |
| 20971 | GET | `/api/developer/monitoring/status` | Y | Y | - | - | - |
| 21036 | GET | `/api/developer/backups/list` | Y | Y | - | - | - |
| 21081 | POST | `/api/developer/test-data/generate` | Y | Y | - | - | - |
| 21219 | GET | `/api/users/developer` | - | Y | - | - | - |
| 21237 | GET | `/api/developer/logs/view` | Y | Y | - | - | - |
| 21315 | POST | `/api/developer/tests/verbose` | Y | Y | - | - | - |
| 21399 | GET | `/api/developer/diagnostics` | Y | Y | - | - | - |
| 21520 | GET | `/api/user/preferred-name` | Y | - | - | - | - |
| 21551 | POST | `/api/wellness/log` | Y | - | - | - | - |
| 21633 | GET | `/api/wellness/today` | Y | - | - | - | - |
| 21680 | GET | `/api/wellness/summary` | Y | - | - | - | - |
| 21740 | GET | `/api/user/medications` | Y | - | - | - | - |
| 21798 | POST | `/api/user/medications` | Y | - | - | - | - |
| 21842 | PUT | `/api/user/medications/<int:med_id>` | Y | - | - | - | - |
| 21885 | DELETE | `/api/user/medications/<int:med_id>` | Y | - | - | - | - |
| 21909 | POST | `/api/user/medications/<int:med_id>/log` | Y | - | - | - | - |
| 21960 | GET | `/api/user/medications/adherence` | Y | - | - | - | - |
| 22001 | GET | `/api/clinician/patient/<patient_username>/medications` | Y | Y | Y | - | - |
| 22057 | GET | `/api/user/quests` | Y | - | - | - | - |
| 22160 | POST | `/api/user/quests/accept` | Y | - | - | - | - |
| 22214 | POST | `/api/user/quests/<int:quest_id>/abandon` | Y | - | - | - | - |
| 22234 | GET | `/api/clinician/patient/<patient_username>/quests` | Y | Y | - | - | - |
| 22281 | POST | `/api/clinician/patient/<patient_username>/quests/assign` | Y | Y | - | - | - |
| 22341 | POST | `/api/user/spell/cast` | Y | - | - | - | - |
| 22394 | GET | `/api/user/spells` | Y | - | - | - | - |
| 22443 | GET | `/api/clinician/waiting-list` | Y | Y | - | - | - |
| 22485 | POST | `/api/clinician/waiting-list` | Y | Y | - | - | - |
| 22537 | PUT | `/api/clinician/waiting-list/<int:entry_id>` | Y | - | - | - | - |
| 22571 | POST | `/api/clinician/waiting-list/<int:entry_id>/convert` | Y | - | - | - | - |
| 22601 | DELETE | `/api/clinician/waiting-list/<int:entry_id>` | Y | - | - | - | - |
| 22744 | GET | `/api/user/progress-dashboard` | Y | - | - | - | - |
| 22893 | POST | `/api/clinician/patient/<patient_username>/milestone-message` | Y | Y | - | - | - |
| 22927 | GET | `/api/clinician/patient/<patient_username>/progress-dashboard` | Y | Y | - | - | - |
| 23003 | GET | `/api/homework/current` | Y | - | - | - | - |
| 23350 | POST | `/api/activity/log` | Y | - | - | - | - |
| 23416 | GET | `/api/activity/consent` | Y | - | - | - | - |
| 23448 | POST | `/api/activity/consent` | Y | - | - | - | - |
| 23492 | POST | `/api/ai/memory/update` | Y | - | - | - | - |
| 23551 | GET | `/api/ai/memory` | Y | - | - | - | - |
| 23567 | POST | `/api/ai/patterns/detect` | - | Y | - | - | - |
| 23669 | POST | `/api/clinician/summaries/generate` | - | - | - | - | - |
| 23773 | GET | `/api/clinician/summaries` | Y | Y | - | - | - |
| 23847 | GET | `/api/clinician/pending-approvals` | Y | Y | - | - | - |
| 23926 | POST | `/api/clinician/approve-patient` | Y | Y | - | - | - |
| 24026 | POST | `/api/clinician/reject-patient` | Y | Y | - | - | - |
| 24114 | GET | `/api/clinician/summary` | Y | Y | - | - | - |
| 24210 | GET | `/api/clinician/patients` | Y | Y | - | - | - |
| 24291 | GET | `/api/clinician/patients/search` | Y | Y | - | - | - |
| 24430 | GET | `/api/clinician/patient/<patient_username>` | Y | Y | - | - | - |
| 24547 | GET | `/api/clinician/patient/<patient_username>/mood-logs` | Y | Y | - | - | - |
| 24662 | GET | `/api/clinician/patient/<patient_username>/analytics` | Y | Y | - | - | - |
| 24752 | GET | `/api/clinician/patient/<patient_username>/assessments` | Y | Y | - | - | - |
| 24854 | GET | `/api/clinician/patient/<patient_username>/sessions` | Y | Y | - | - | - |
| 24934 | GET | `/api/clinician/risk-alerts` | Y | Y | - | - | - |
| 25019 | GET | `/api/clinician/patient/<patient_username>/appointments` | Y | Y | - | - | - |
| 25086 | POST | `/api/clinician/message` | Y | Y | - | - | - |
| 25177 | POST | `/api/wins/log` | Y | - | - | - | - |
| 25245 | GET | `/api/wins/recent` | Y | - | - | - | - |
| 25292 | GET | `/api/wins/stats` | Y | Y | - | - | - |
| 25377 | POST | `/api/suggestions` | Y | - | - | Y | Y |
| 25446 | GET | `/api/suggestions` | Y | - | - | - | - |
| 25474 | DELETE | `/api/suggestions/<int:suggestion_id>` | Y | - | - | Y | - |
| 25512 | POST | `/api/c-ssrs/start` | Y | - | - | - | - |
| 25547 | POST | `/api/c-ssrs/submit` | Y | - | - | - | - |
| 25721 | GET | `/api/c-ssrs/history` | Y | - | - | - | - |
| 25762 | GET | `/api/c-ssrs/<int:assessment_id>` | Y | - | - | - | - |
| 25824 | POST | `/api/c-ssrs/<int:assessment_id>/clinician-response` | Y | - | - | - | - |
| 25875 | POST | `/api/c-ssrs/<int:assessment_id>/safety-plan` | Y | - | - | - | - |
| 25992 | POST | `/api/crisis/detect` | Y | - | - | - | - |
| 26082 | GET | `/api/crisis/alerts` | Y | Y | - | - | - |
| 26154 | POST | `/api/crisis/alerts/<int:alert_id>/acknowledge` | Y | - | - | - | - |
| 26221 | POST | `/api/crisis/alerts/<int:alert_id>/resolve` | Y | - | - | - | - |
| 26279 | GET,POST,PUT,DELETE | `/api/crisis/contacts` | Y | - | - | - | - |
| 26441 | GET | `/api/crisis/coping-strategies` | Y | - | - | - | - |
| 26551 | GET | `/api/clinician/session-notes/<patient_username>` | Y | Y | - | - | - |
| 26597 | POST | `/api/clinician/session-notes` | Y | Y | - | - | - |
| 26646 | PUT | `/api/clinician/session-notes/<int:note_id>` | Y | Y | - | - | - |
| 26708 | POST | `/api/clinician/session-notes/<int:note_id>/sign-off` | Y | Y | - | - | - |
| 26746 | GET | `/api/clinician/treatment-plan/<patient_username>` | Y | Y | - | - | - |
| 26798 | GET | `/api/clinician/treatment-plan/<patient_username>/history` | Y | Y | - | - | - |
| 26825 | POST | `/api/clinician/treatment-plan` | Y | Y | - | - | - |
| 26881 | PUT | `/api/clinician/treatment-plan/<int:plan_id>` | Y | Y | - | - | - |
| 26939 | POST | `/api/clinician/treatment-plan/<int:plan_id>/sign` | Y | Y | - | - | - |
| 26971 | POST | `/api/patient/treatment-plan/sign` | Y | Y | - | - | - |
| 27007 | POST | `/api/patient/treatment-plan/decline` | Y | Y | - | - | - |
| 27041 | GET | `/api/patient/treatment-plan` | Y | Y | - | - | - |
| 27084 | POST | `/api/patient/outcome-measure` | Y | Y | - | - | - |
| 27161 | POST | `/api/clinician/outcome-measure` | Y | Y | - | - | - |
| 27202 | GET | `/api/clinician/patient/<patient_username>/outcome-measures` | Y | Y | - | - | - |
| 27236 | GET | `/api/patient/outcome-measures` | Y | Y | - | - | - |
| 27269 | POST | `/api/patient/crisis-alert` | Y | - | - | Y | - |
| 27324 | GET | `/api/clinician/caseload/outcome-summary` | Y | Y | - | - | - |
| 27376 | PUT | `/api/clinician/treatment-plan/<int:plan_id>/goal/<int:goal_index>` | Y | Y | - | Y | - |
