import unittest
import app as app_module
class EndToEndSmokeTests(unittest.TestCase):
    def setUp(self): app_module.app.config['TESTING']=True; self.client=app_module.app.test_client()
    def test_health_home_platform(self):
        self.assertEqual(self.client.get('/health').status_code,200); self.assertEqual(self.client.get('/').status_code,200); self.assertEqual(self.client.get('/api/platform/status').status_code,200)
    def test_vocabulary_and_sequence(self):
        self.assertEqual(self.client.get('/api/vocabulary').status_code,200); r=self.client.post('/api/sequence/decode',json={'predictions':[{'label':'OPEN_PALM','stability':.9},{'label':'OPEN_PALM','stability':.9},{'label':'THUMBS_UP','stability':.8}]}); self.assertEqual(r.status_code,200); self.assertEqual(r.get_json()['tokens'],['OPEN_PALM','THUMBS_UP'])
if __name__=='__main__': unittest.main()
