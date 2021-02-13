from const import *

class VMWriter:
    def __init__(self, output_vm_file_path):
        self.wf = open(output_vm_file_path, 'w')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return self.wf.close()

    def write_push(self, segment, index):
        segment_name = self._get_segment_name(segment)
        self.wf.write('push {} {}\n'.format(segment_name, index))

    def write_pop(self, segment, index):
        segment_name = self._get_segment_name(segment)
        self.wf.write('pop {} {}\n'.format(segment_name, index))
    
    def write_arithmetic(self, command):
        if command == ArithmeticType.ADD:
            self.write_code('add')
        elif command == ArithmeticType.SUB:
            self.write_code('sub')
        elif command == ArithmeticType.NEG:
            self.write_code('neg')
        elif command == ArithmeticType.EQ:
            self.write_code('eq')
        elif command == ArithmeticType.GT:
            self.write_code('gt')
        elif command == ArithmeticType.LT:
            self.write_code('lt')
        elif command == ArithmeticType.AND:
            self.write_code('and')
        elif command == ArithmeticType.OR:
            self.write_code('or')
        elif command == ArithmeticType.NOT:
            self.write_code('not')
        else:
            raise ValueError('Invalid arithmetic number.')

    def write_label(self, label):
        self.wf.write('label {}\n'.format(label))

    def write_goto(self, label):
        self.wf.write('goto {}\n'.format(label))

    def write_if(self, label):
        self.wf.write('if-goto {}\n'.format(label))

    def write_call(self, name, n_args):
        self.wf.write('call {} {}\n'.format(name, n_args))

    def write_function(self, name, n_locals):
        self.wf.write('function {} {}\n'.format(name, n_locals))

    def write_return(self):
        self.write_code('return')
        self.write_code('\n')

    def write_code(self, code):
        self.wf.write('{}\n'.format(code))

    def _get_segment_name(self, segment):
        if segment == SegmentType.CONST:
            return 'constant'
        elif segment == SegmentType.ARG:
            return 'argument'
        elif segment == SegmentType.LOCAL:
            return 'local'
        elif segment == SegmentType.STATIC:
            return 'static'
        elif segment == SegmentType.THIS:
            return 'this'
        elif segment == SegmentType.THAT:
            return 'that'
        elif segment == SegmentType.POINTER:
            return 'pointer'
        elif segment == SegmentType.TEMP:
            return 'temp'
        else:
            raise ValueError('Invalid segment number.')
