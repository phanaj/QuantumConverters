NAME_MAP = {
	'H':      'h',
	'I':      'id',
	'S':      's',
	'T':      't',
	'X':      'x',
	'Y':      'y',
	'Z':      'z',
	'CZ':     'cz',
	'RX':     'rx',
	'RY':     'ry',
	'RZ':     'rz',
	'CNOT':   'cx',
	'CCNOT':  'ccx',
	'SWAP':   'swap',
	'PHASE':  'u1',
	'CSWAP':  'cswap',
	'CPHASE': 'crz'
}

def get_handlers(QQ):
	handlers = {
		'H':       QQ.simple_gate,
		'I':       QQ.simple_gate,
		'S':       QQ.simple_gate,
		'T':       QQ.simple_gate,
		'X':       QQ.simple_gate,
		'Y':       QQ.simple_gate,
		'Z':       QQ.simple_gate,
		'CZ':      QQ.simple_gate,
		'CNOT':    QQ.simple_gate,
		'CCNOT':   QQ.simple_gate,
		'SWAP':    QQ.simple_gate,
		'CSWAP':   QQ.simple_gate,
		'RX':      QQ.param_gate,
		'RY':      QQ.param_gate,
		'RZ':      QQ.param_gate,
		'PHASE':   QQ.param_gate,
		'CPHASE':  QQ.param_gate,
		'DECLARE': QQ.declare,
		'MEASURE': QQ.measure,
		'RESET':   QQ.reset,
		'#':       QQ.comment
	}
	return handlers
