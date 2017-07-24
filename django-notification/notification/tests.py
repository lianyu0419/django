#coding=utf-8
""" test all
"""

from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User as DjangoUser
from django.core.urlresolvers import reverse
from django.utils import simplejson
from notification.models import Notice, NoticeType, NoticeSetting, create_notice_type



class TestNoticeType(unittest.TestCase):
    def setUp(self):
        self.user = DjangoUser.objects.create_user(username="ggg")
        self.notice_type = create_notice_type("models new", "new task added", "task")
        
    def tearDown(self):
        self.user.delete()
        self.notice_type.delete()
    
    def test_create_notice_type(self):
        notice_type = create_notice_type("task new", "new task added", "task")
        notice_types = NoticeType.objects.filter(label=notice_type.label)
        self.assertEqual(len(notice_types), 1)
        
        notice_type.delete()
            
    def test_create_notice_type_with_same(self):
        notice_type = create_notice_type("task new", "new task added", "task")
        notice_type1 = create_notice_type("task new", "new task added11", "task")
        notice_types = NoticeType.objects.filter(label=notice_type.label)
        self.assertEqual(len(notice_types), 1)
        
        notice_type.delete()
    
        

class TestNotice(unittest.TestCase):
    def setUp(self):
        self.user = DjangoUser.objects.create_user(username="ggg")
        self.notice_type = create_notice_type("models new", "new task added", "task")
        
    def tearDown(self):
        self.user.delete()
        self.notice_type.delete()
        
    def test_notice_is_could_send(self):
        notice = Notice.push(self.user, self.notice_type, "http://www.baidu.com", "ffgg")
        self.assertTrue(notice.is_could_send(NoticeSetting.DEVICE_WEB))
        
        notice.delete()
        
    def test_unread(self):
        notice = Notice.push(self.user, self.notice_type, "http://www.baidu.com", "ffgg")
        notices = Notice.objects.unread(self.user, NoticeSetting.DEVICE_WEB)
        self.assertEqual(len(notices), 1)
        
        notice.delete()
    
    def test_unread_with_read(self):
        notice = Notice.push(self.user, self.notice_type, "http://www.baidu.com", "ffgg", is_read=True)
        notices = Notice.objects.unread(self.user, NoticeSetting.DEVICE_WEB)
        self.assertEqual(len(notices), 0)
        
        notice.delete()
        
    def test_unread_and_unsend(self):
        notice = Notice.push(self.user, self.notice_type, "http://www.baidu.com", "ffgg")
        notices = Notice.objects.unread_and_unsend(self.user, NoticeSetting.DEVICE_WEB)
        self.assertEqual(len(notices), 1)
        
        notices = Notice.objects.unread_and_unsend(self.user, NoticeSetting.DEVICE_EMAIL)
        self.assertEqual(len(notices), 0)
        
        notice.delete()
    
    
    def test_unread_and_unsend_with_sent(self):
        notice = Notice.push(self.user, self.notice_type, "http://www.baidu.com", "ffgg", sent_device=2)
        notices = Notice.objects.unread_and_unsend(self.user, NoticeSetting.DEVICE_WEB)
        self.assertEqual(len(notices), 1)
        
        notices = Notice.objects.unread_and_unsend(self.user, NoticeSetting.DEVICE_EMAIL)
        self.assertEqual(len(notices), 0)
        
        notice.delete()
    
    def test_push(self):
        target = "dddd"
        content = "gggg"
        
        notice = Notice.push(self.user, self.notice_type, target, content)
        notice1 = Notice.push(self.user, self.notice_type, target, content)
        self.assertEqual(notice, notice1)
        
        notice.delete()
        
    def test_send_to_email(self):
        target = "dddd"
        content = "gggg"
        self.notice_type.flags = 3
        self.notice_type.save()
        notice = Notice.push(self.user, self.notice_type, target, content)
        
        Notice.send_to_email(self.user)
        
        new_notice = Notice.objects.get(id=notice.id)
        self.assertEqual(new_notice.sent_device, 2)
        
        self.notice_type.flags = 1
        self.notice_type.save()
        notice.delete()
                
        
class TestViews(unittest.TestCase):
    def setUp(self):
        self.user = DjangoUser.objects.create_user(username="ggg", password="ggg")
        self.notice_type = create_notice_type("task_new", "new task added", "task")
        self.client = Client()
        self.client.login(username=self.user.username, password=self.user.username)
        
    def tearDown(self):
        self.user.delete()
        self.notice_type.delete()
    
    def test_home(self):
        notice = Notice.push(user=self.user, notice_type=self.notice_type, target="http://www.baidu.com",
                             content=u"ggg")
        url = reverse("notification.views.home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        
        notice.delete()
        
    def test_change(self):
        url = reverse("notification.views.change")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        
    def test_change_with_post(self):
        url = reverse("notification.views.change")
        data = {self.notice_type.label:(0, 1)}
        resp = self.client.post(url, data)
        self.assertEqual(resp.status_code, 302)
        
        notice_setting = NoticeSetting.objects.get(user=self.user, notice_type=self.notice_type)
        self.assertEqual(notice_setting.devices_tuple(), data[self.notice_type.label])
        
    def test_go(self):
        notice = Notice.push(user=self.user, notice_type=self.notice_type, target="http://www.baidu.com",
                             content=u"ggg")
        url = reverse("notification.views.go", args=[notice.id])
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 302)
        
        notice.delete()
        
    def test_my(self):
        notice = Notice.push(user=self.user, notice_type=self.notice_type, target="http://www.baidu.com",
                             content=u"ggg")
        url = reverse("notification.views.my")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        
        result = simplejson.loads(resp.content)
        self.assertTrue(result["is_ok"])
        
        notice.delete()
        
    def test_clear(self):
        notice = Notice.push(user=self.user, notice_type=self.notice_type, target="http://www.baidu.com",
                             content=u"ggg")
        url = reverse("notification.views.clear")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        
        notices = Notice.objects.unread_of_email(self.user)
        self.assertEqual(len(notices), 0)
        
        notice.delete()