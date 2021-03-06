# -*- coding: utf-8 -*-
from django.conf import settings

from tcms.core.utils.mailto import mailto


def email_plan_update(plan):
    recipients = get_plan_notification_recipients(plan)
    if len(recipients) == 0:
        return
    subject = 'TestPlan %s has been updated.' % plan.pk
    mailto(settings.PLAN_EMAIL_TEMPLATE, subject, recipients,
           context={'plan': plan})


def email_plan_deletion(plan):
    recipients = get_plan_notification_recipients(plan)
    if len(recipients) == 0:
        return
    subject = 'TestPlan %s has been deleted.' % plan.pk
    mailto(settings.PLAN_DELELE_EMAIL_TEMPLATE, subject, recipients,
           context={'plan': plan})


def get_plan_notification_recipients(plan):
    recipients = set()
    if plan.owner:
        if plan.email_settings.auto_to_plan_owner:
            recipients.add(plan.owner.email)
    if plan.email_settings.auto_to_plan_author:
        recipients.add(plan.author.email)
    if plan.email_settings.auto_to_case_owner:
        case_authors = plan.case.values_list('author__email', flat=True)
        recipients.update(case_authors)
    if plan.email_settings.auto_to_case_default_tester:
        case_testers = plan.case.values_list('default_tester__email',
                                             flat=True)
        recipients.update(case_testers)
    return [r for r in recipients if r]
