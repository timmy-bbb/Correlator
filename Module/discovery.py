
from mako.template import Template

from common.event import NoticeEvent, ErrorEvent, EventProcessor, AuditEvent
from common.util import Module, format_timestamp


class DiscoveryStatsEvent(AuditEvent):

    audit_id = 'module-stats'
    fields = [
        'num_discoveries'
    ]

    def __init__(self, data):
        super().__init__(self.audit_id, data)

        self.template_txt = Template(
            '${num_discoveries} total discoveries.')


class Discovery(Module):

    def __init__(self, processor: EventProcessor, log):

        self.log = log
        self.processor = processor
        self.description = 'Discovery'
        self.identifier = 'Discovery'
        self.module_name = self.identifier

        self.states = {}
        self.log = log

        self.discoveries = 0

    def clear_statistics(self):
        self.discoveries = 0

    def statistics(self, reset=False):

        data = {
            'num_discoveries': self.discoveries
        }
        self.dispatch_event(DiscoveryStatsEvent(data))

        if reset:
            self.clear_statistics()

    def _setstate(self, identifier, state):
        self.states[identifier] = state
        return state

    def _get_state(self, identifier):

        state = self.states.get(identifier)
        if state is None:
            return self._setstate(identifier, 0)
        return state

        # Create and update transactions store

    @staticmethod
    def tostring(record):
        return f'{record.timestamp} {record.hostname} {record.instance} {record.prog} {record.identifier} {record.msgid} {record.detail}'

    def process_iddiscover(self, record):
        print(f'IDDISCOVER: {self.tostring(record)}')

    def process_psupdate(self, record):
        print(f'PSUPDATE: {self.tostring(record)}')

    def process_iddb(self, record):
        print(f'IDDB: {self.tostring(record)}')
    def process_record(self, record):

        if record.prog.startswith('psupdate.exe'):
            self.process_psupdate(record)
        elif record.prog.startswith('iddiscover.exe'):
            self.process_iddiscover(record)
        elif record.prog.startswith('iddb.exe'):
            self.process_iddb(record)

        return True

