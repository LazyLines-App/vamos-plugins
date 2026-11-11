---
type: regex
target: last_message
pattern: 'instagram\.com/p/(?!(?:De49HQvgUbF|De78Pr4DABW|De7a_Gqk\-sY|De9czaFgIqc|DeUO0ZSRbtr|De\-jmrfPgtt|Decg9hJjK_D|DedCMT7Monb|Def3urhtaGC|DeiQ23GDqjJ|DekNNihDxdc|DekiD\-zive1|DekwR25lJgt|DemP8MaD20j|Demyf2QE7X0|DepEkkyicTR|DepaKIVD2IS|DesuEsUNfk2|DeuNdmmkT3w|Dex25GQj9Uz|DexbI1Fhcv_|DfAIU7HxeAQ|DfDD57jAQ44|DfFoUcNjUPY|DfH7xYogP\-_|DfNDxQ7PpaK|DfNaiUypqZs|DfNsJ5jDl5F|DfOQZKsCq\-G|DfP7L2WDNSY|DfPfuoZgb0z|DfQPthjgKvd|DfSUO0CDCCm|DfVSdbGDNMM|DfVnVB7jXF\-|DfVzofmAND0|DfYTnaJFcMP|DffxQyBjSVQ|DfiCCKNHMo8|DfkCsRMknwQ)(?![\w-]))[\w-]+'
match: not_contains
---
# Every post link is one the rows or the answer gave. (?![\w-]) not \b: some ids end in '-'.
