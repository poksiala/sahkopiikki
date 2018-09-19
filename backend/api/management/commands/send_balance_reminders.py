"""Send balance reminders"""
import json
import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from api.models import UserProfile

class Command(BaseCommand):
  """Command"""
  help = 'Sends balance reminders to slack.'

  @staticmethod
  def compose_message(base_message: dict, profile: UserProfile, debug=False) -> dict:
    """Compose message"""
    assert base_message.get('text'), '`base_message` must contain `text` field'
    message = dict(base_message)
    message['text'] = message['text'].format(
        name=profile.user.first_name, balance=profile.balance())
    if not debug:
      message['channel'] = "@{}".format(profile.slack_handle)
    return message

  def construct_messages(self, queryset, **kwargs) -> list:
    """Construct messages

    Results in a list of dicts that contain payloads for webhook requests. The effects
    of `--ignore-debug`, `--report-zero-balance` and `--slack-handle` are handled here.
    """
    ignore_debug = kwargs['ignore_debug']
    slack_handle = kwargs['slack_handle']
    report_zero_balance = kwargs['report_zero_balance']

    results = list()
    debug = settings.DEBUG and not (ignore_debug or slack_handle)

    if debug:
      self.stdout.write("DEBUG is on. All messages will be sent to webhook's default channel")

    if slack_handle: # Filter queryset if `--slack-handle` option was used
      queryset = queryset.filter(slack_handle=slack_handle)
      if queryset.count() == 0:
        self.stderr.write(
            'There is no `UserProfile` in the database with handle `{}`'.format(slack_handle))

    for profile in queryset:
      if profile.balance_cents() or report_zero_balance:
        results.append(self.compose_message(settings.SLACK_DICT, profile, debug))
    return results

  def send_notifications(self, messages: list, dry_run=False) -> int:
    """Send notifications"""
    successfuly_sent = 0
    for message in messages:
      payload = json.dumps(message)
      if dry_run:
        self.stdout.write(payload)
        continue
      response = requests.post(settings.SLACK_WEBHOOK_URL, data=payload)
      if response.status_code == 200:
        successfuly_sent += 1
      else:
        self.stderr.write("{}\n{}".format(response.status_code, response.text))
    return successfuly_sent

  def add_arguments(self, parser):
    parser.add_argument(
        '--slack-handle', type=str, dest='slack_handle',
        help='Send notification only to given slack_handle even in debug mode')
    parser.add_argument(
        '--ignore-debug', action='store_true', dest='ignore_debug',
        help='Ignore debug mode completely and send notifications for real')
    parser.add_argument(
        '--report-zero-balance', action='store_true', dest='report_zero_balance',
        help='Send notifications even if users balance is zero')
    parser.add_argument(
        '--dry-run', action='store_true', dest='dry_run',
        help='Do not sent messages, just print payloads')

  def handle(self, *args, **options):
    if not settings.SLACK_WEBHOOK_URL:
      raise CommandError('SLACK_WEBHOOK_URL not configured. Please refer to the README')

    user_profiles = UserProfile.objects.exclude(slack_handle__isnull=True)
    messages = self.construct_messages(user_profiles, **options)
    successfuly_sent = self.send_notifications(messages, dry_run=options['dry_run'])
    self.stdout.write(self.style.SUCCESS(
        '{} messages were successfully sent.'.format(successfuly_sent)))
