from mln.models.static import MessageBody
from mln.services.message import create_attachment, delete_message, detach_attachments, easy_reply, open_message, send_message
from mln.tests.services.test_friend import friends
from mln.tests.setup_testcase import cls_setup, requires, setup, TestCase
from mln.tests.test_profile import item, two_users

@cls_setup
def body(cls):
	cls.BODY = MessageBody.objects.create()

@cls_setup
@requires(body)
def other_body(cls):
	cls.REPLY_BODY = MessageBody.objects.create()

@cls_setup
@requires(other_body)
def easy_reply_body(cls):
	cls.BODY.easy_replies.add(cls.REPLY_BODY)

@setup
@requires(body, two_users)
def message(self):
	self.message = self.user.messages.create(sender=self.other_user, body_id=self.BODY.id)

@setup
@requires(item, two_users)
def other_user_has_item(self):
	self.other_user.profile.add_inv_item(self.ITEM_ID, 1)

@setup
@requires(item, message)
def attachment(self):
	self.message.attachments.create(item_id=self.ITEM_ID, qty=1)

class NoMessageTest(TestCase):
	SETUP = body, two_users

	def test_send_message_no_friend(self):
		with self.assertRaises(RuntimeError):
			send_message(self.user, self.other_user.id, self.BODY.id)

class NoMessageFriendTest(TestCase):
	SETUP = body, friends

	def test_send_message_ok(self):
		message = send_message(self.user, self.other_user.id, self.BODY.id)
		self.assertTrue(self.other_user.messages.filter(id=message.id, sender_id=self.user.id, body_id=self.BODY.id).exists())

class MessageTest(TestCase):
	SETUP = message,

	def test_delete_message_wrong_user(self):
		with self.assertRaises(RuntimeError):
			detach_attachments(self.other_user, self.message.id)

	def test_detach_attachments_wrong_user(self):
		with self.assertRaises(RuntimeError):
			detach_attachments(self.other_user, self.message.id)

	def test_open_message_already_read(self):
		self.message.is_read = True
		self.message.save()
		open_message(self.user, self.message.id)
		self.assertTrue(self.user.messages.get(id=self.message.id).is_read)

	def test_open_message_ok(self):
		open_message(self.user, self.message.id)
		self.assertTrue(self.user.messages.get(id=self.message.id).is_read)

class CreateAttachmentNoStackTest(TestCase):
	SETUP = message, item

	def test_create_attachment_no_stack(self):
		with self.assertRaises(RuntimeError):
			create_attachment(self.message, self.ITEM_ID, 1)

class CreateAttachmentExistingStackTest(TestCase):
	SETUP = other_user_has_item, message

	def test_create_attachment_ok(self):
		create_attachment(self.message, self.ITEM_ID, 1)
		self.assertFalse(self.other_user.inventory.filter(id=self.ITEM_ID).exists())
		self.assertTrue(self.message.attachments.filter(item_id=self.ITEM_ID, qty=1).exists())

class ExistingAttachmentTest(TestCase):
	SETUP = attachment,

	def check_detach_attachments(self):
		self.assertFalse(self.message.attachments.all().exists())
		self.assertTrue(self.user.inventory.filter(item_id=self.ITEM_ID, qty=1).exists())

	def test_delete_message_ok(self):
		delete_message(self.user, self.message.id)
		self.check_detach_attachments()
		self.assertFalse(self.user.messages.filter(id=self.message.id).exists())

	def test_detach_attachments_ok(self):
		detach_attachments(self.user, self.message.id)
		self.check_detach_attachments()

class EasyReplyNoFriendTest(TestCase):
	SETUP = easy_reply_body, message

	def test_easy_reply_no_friend(self):
		with self.assertRaises(RuntimeError):
			easy_reply(self.user, self.other_user.id, self.BODY.id, self.REPLY_BODY.id)

class EasyReplyNoMessageTest(TestCase):
	SETUP = easy_reply_body, friends

	def test_easy_reply_no_message(self):
		with self.assertRaises(RuntimeError):
			easy_reply(self.user, self.other_user.id, self.BODY.id, self.REPLY_BODY.id)

class EasyReplyNotAnEasyReplyTest(TestCase):
	SETUP = other_body, message, friends

	def test_easy_reply_not_an_easy_reply(self):
		with self.assertRaises(RuntimeError):
			easy_reply(self.user, self.other_user.id, self.BODY.id, self.REPLY_BODY.id)

class EasyReplyFriendTest(TestCase):
	SETUP = easy_reply_body, message, friends

	def test_easy_reply_ok(self):
		easy_reply(self.user, self.other_user.id, self.BODY.id, self.REPLY_BODY.id)
		self.assertTrue(self.other_user.messages.filter(sender=self.user, body=self.REPLY_BODY).exists())