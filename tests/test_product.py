import unittest

import app as live_app
from src.gesture_engine import DynamicGestureTracker, SentenceBuilder, classify_static


def hand(states):
    # Simple synthetic MediaPipe-like coordinates. states = thumb,index,middle,ring,pinky.
    pts=[[.5,.9] for _ in range(21)]
    # thumb MCP-ish / tip: right hand open means tip x < joint x
    pts[3]=[.42,.7];pts[4]=[.28 if states[0] else .48,.68]
    for ext,tip,pip,x in zip(states[1:],[8,12,16,20],[6,10,14,18],[.43,.5,.57,.64]):
        pts[pip]=[x,.58];pts[tip]=[x,.28 if ext else .74]
    return pts


class ProductTests(unittest.TestCase):
    def setUp(self):
        live_app.app.config.update(TESTING=True)
        self.client=live_app.app.test_client()
        live_app.tracker.x.clear();live_app.smoother.labels.clear();live_app.sentence.clear()

    def test_static_vocabulary(self):
        self.assertEqual(classify_static(hand([1,1,1,1,1]))['label'],'OPEN_PALM')
        self.assertEqual(classify_static(hand([0,0,0,0,0]))['label'],'FIST')
        self.assertEqual(classify_static(hand([0,1,1,0,0]))['label'],'V_SIGN')
        self.assertEqual(classify_static(hand([1,0,0,0,0]))['label'],'THUMBS_UP')

    def test_dynamic_swipe(self):
        tracker=DynamicGestureTracker(window=4,threshold=.2)
        result=None
        for x in [.2,.3,.4,.55]:
            pts=hand([1,1,1,1,1]);pts[0]=[x,.9];result=tracker.update(pts)
        self.assertEqual(result,'SWIPE_RIGHT')

    def test_sentence_debounce(self):
        b=SentenceBuilder();self.assertEqual(b.push('OPEN_PALM'),'hello');self.assertEqual(b.push('OPEN_PALM'),'hello');b.reset_debounce();self.assertEqual(b.push('OPEN_PALM'),'hello hello')

    def test_api_predicts(self):
        r=self.client.post('/api/predict',json={'landmarks':hand([1,0,0,0,0]),'handedness':'Right'})
        self.assertEqual(r.status_code,200);self.assertEqual(r.get_json()['raw_label'],'THUMBS_UP')

    def test_rejects_bad_landmarks(self):
        self.assertEqual(self.client.post('/api/predict',json={'landmarks':[[0,0]]}).status_code,400)


if __name__=='__main__':unittest.main()
