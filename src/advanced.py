from collections import Counter
from pathlib import Path
from flask import Blueprint, jsonify, request
from .sample_store import load_samples

BUILT_IN=['OPEN_PALM','FIST','POINT','V_SIGN','THUMBS_UP','I_LOVE_YOU','SWIPE_LEFT','SWIPE_RIGHT']

def vocabulary_status(sample_path='training_data/landmarks.jsonl',minimum_per_label=25):
    rows=load_samples(Path(sample_path)); counts=Counter(r['label'] for r in rows); labels=sorted(set(BUILT_IN)|set(counts)); return {'labels':[{'label':x,'samples':counts.get(x,0),'train_ready':counts.get(x,0)>=minimum_per_label,'source':'built-in+learned' if x in BUILT_IN and counts.get(x) else 'built-in' if x in BUILT_IN else 'learned'} for x in labels],'total_samples':len(rows),'minimum_samples_per_label':minimum_per_label}

def decode_sequence(predictions,min_stability=.6):
    out=[]; last=None
    for item in predictions:
        label=str(item.get('label','')).strip(); stability=float(item.get('stability',item.get('confidence',1)))
        if not label or stability<min_stability or label==last: continue
        out.append(label); last=label
    return {'tokens':out,'text':' '.join(x.replace('_',' ').lower() for x in out)}

def register_advanced(app):
    bp=Blueprint('signflow_advanced',__name__)
    @bp.get('/api/vocabulary')
    def vocabulary(): return jsonify(vocabulary_status())
    @bp.post('/api/sequence/decode')
    def sequence_decode():
        p=request.get_json(silent=True) or {}
        try: return jsonify(decode_sequence(p.get('predictions') or [],float(p.get('min_stability',.6))))
        except (TypeError,ValueError) as exc: return jsonify({'error':str(exc)}),400
    app.register_blueprint(bp)
