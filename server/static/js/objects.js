// List of "supported' objects with number of inlets and outlets

var objectDictionary = {
	'osc~'		: {inlets: 2, outlets: 1},
	'mtof'		: {inlets: 1, outlets: 1},
	'random'	: {inlets: 2, outlets: 1},
	'metro'		: {inlets: 2, outlets: 1},
	'+'			: {inlets: 2, outlets: 1},
	'phasor~'	: {inlets: 2, outlets: 1},
	'*'			: {inlets: 2, outlets: 1},
	'*~'		: {inlets: 2, outlets: 1},
	'+~'		: {inlets: 2, outlets: 1},
	'/'			: {inlets: 2, outlets: 1},
	'/~'		: {inlets: 2, outlets: 1},
	'expr'		: {inlets: 1, outlets: 1},
	'expr~'		: {inlets: 1, outlets: 1},
	'float'		: {inlets: 2, outlets: 1},
	'f'			: {inlets: 2, outlets: 1},
	'select'	: {inlets: 2, outlets: 2}, // TODO: has dynamic outlets
	'>'			: {inlets: 2, outlets: 1},
	'<'			: {inlets: 2, outlets: 1},
	'>='		: {inlets: 2, outlets: 1},
	'<='		: {inlets: 2, outlets: 1},
	'=='		: {inlets: 2, outlets: 1},
	'delay'		: {inlets: 2, outlets: 1},
	'timer'		: {inlets: 2, outlets: 1},
	'pipe'		: {inlets: 2, outlets: 1},
	'trigger'	: {inlets: 1, outlets: 2}, // TODO: has dynamic outlets
	't'			: {inlets: 1, outlets: 2}, // TODO: has dynamic outlets
	'send'		: {inlets: 1, outlets: 0},
	's'			: {inlets: 1, outlets: 0},
	'send~'		: {inlets: 1, outlets: 0},
	'receive'	: {inlets: 0, outlets: 1},
	'r'			: {inlets: 0, outlets: 1},
	'receive~'	: {inlets: 0, outlets: 1},
	'pack'		: {inlets: 2, outlets: 1}, // TODO: has dynamic inlets
	'unpack'	: {inlets: 1, outlets: 2}, // TODO: has dynamic outlets
	'print'		: {inlets: 1, outlets: 0}, // for debugging purposes
};
