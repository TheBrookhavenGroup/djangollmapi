from datetime import date, timedelta
from django.test import TestCase, Client, tag
from django.conf import settings
from users.models import Member
from apis.models import ApiKey
from .multi import sequential_query, run_parallel_query


class ApiBaseTest(TestCase):
    def setUp(self):
        Member.objects.create_user(email='foo@foobar.com', password='12345')
        a = ApiKey.objects.create(email='goo@goobar.com')
        a.start_date = date.today()
        a.end_date = a.start_date + timedelta(days=1)
        a.save()

        self.key_obj = a

        self.client = Client()
        self.header = {'Authorization': f'Bearer {a.key}'}

        settings.LLM_PACKAGE = 'tbg_llm_example'
        settings.LLM_MODELS = ["EleutherAI/pythia-410m",
                               "EleutherAI/pythia-410m"]


class TestPermissions(ApiBaseTest):

    def post_it(self, data):
        return self.client.post('/permission_test/',
                                headers=self.header,
                                data=data)

    def test_split(self):
        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'Hello, World!'})

    def test_n(self):
        self.key_obj.n_requests = self.key_obj.n_allowed_requests
        self.key_obj.save()

        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 401)

    def test_date(self):
        ko = self.key_obj
        ko.start_date = self.key_obj.end_date
        ko.n_requests = 0
        ko.save()

        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 401)

        ko.start_date = None
        ko.end_date = None
        ko.save()
        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 200)

        ko.start_date = date.today()
        ko.end_date = date.today() + timedelta(days=1)
        ko.save()

        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 200)

    def test_nolimit(self):
        ko = self.key_obj
        ko.n_allowed_requests = None
        ko.n_requests = 10
        ko.start_date = None
        ko.end_date = None
        ko.save()

        response = self.post_it({'text': 'Hello, World!'})
        self.assertEqual(response.status_code, 200)


@tag("inhibit_test")
class TestMulti(ApiBaseTest):
    def setUp(self):
        super().setUp()
        self.data = [
            # ('https://google.com/search?q=hello',
            #  {"User-Agent": "Mozilla/5.0"}, None),
            # ('https://yahoo.com', None, None),
            ('https://httpbin.org/post', None, {'text': 'Hello, World!'}),
            ('https://httpbin.org/get', None, None),
            ('https://api.zippopotam.us/us/21208', None, None),
            ('https://api.zippopotam.us/us/10023', None, None),
        ]

    def test_sequential(self):
        responses = sequential_query(self.data)
        for uhd, response in zip(self.data, responses):
            self.assertEqual(response.status_code, 200, f"Failed for {uhd}")

    def test_parallel(self):
        responses = run_parallel_query(self.data)
        for uhd, response in zip(self.data, responses):
            print(uhd, response)
            self.assertEqual(response.status_code, 200, f"Failed for {uhd}")


class ApiTest(ApiBaseTest):
    def test_api_post(self):
        response = self.client.post('/analyze/',
                                    headers=self.header,
                                    data={'text': 'The quick brown fox'})
        self.assertEqual(response.status_code, 200)
        expected = (b'{"message":"The quick brown fox jumps over"}')
        self.assertEqual(expected, response.content)
