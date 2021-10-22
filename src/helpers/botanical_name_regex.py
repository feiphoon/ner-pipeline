"""
https://kalnytskyi.com/howto/assert-str-matches-regex-in-pytest/

Level 1A - Species, Aggregates & Hybrids only
Vicia faba
Taraxacum officinale agg.
Spartina × townsendii

Level 1B - Species, Aggregates & Hybrids with infraspecific taxa
Vicia sativa subsp. Nigra
Vicia johannis var. Procumbens
Pisum sativum cv. Meteor

Level 2A - Species, Aggregates & Hybrids only, with Authors and References
Vicia faba L.
Taraxacum officinale agg.
Spartina × townsendii H.Groves & J.Groves

Level 2B - Species, Aggregates and Hybrids with Infraspecific Taxa,
and with Authors and References
Vicia sativa subsp. nigra (L.) Ehrh.
Vicia johannis var. procumbens H.I. Schäf.
Pisum sativum L. cv. Meteor
"""

import re
