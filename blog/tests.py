from django.test import TestCase
from .models import Post
from django.contrib.auth.models import User
from django.shortcuts import reverse



class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user1')
        cls.post1 = Post.objects.create(
            title='post1',
            text='this is a discription of post1',
            status=Post.STATUS_CHOICE[0][0],
            author=cls.user,

        )
        cls.post2 = Post.objects.create(
            title='post2',
            text='Lorem Ipsome poste2',
            status=Post.STATUS_CHOICE[1][0],
            author=cls.user,

        )

    # def setUp(self):
    def test_post_modle_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_title(self):
        self.assertEqual(self.post1.title, 'post1')
        self.assertEqual(self.post1.text, 'this is a discription of post1')

    def test_post_list_url(self):
        responce = self.client.get('/blog/')
        self.assertEqual(responce.status_code, 200)

    def test_post_list_by_url_by_name(self):
        responce = self.client.get(reverse('posts_list'))
        self.assertEqual(responce.status_code, 200)

    def test_post_title_on_blog_list_page(self):
        responce = self.client.get(reverse('posts_list'))
        self.assertContains(responce, 'post1')

    def test_post_detail_url(self):
        responce = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(responce.status_code, 200)

    def test_post_detail_url_by_name(self):
        responce = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(responce.status_code, 200)

    def test_post_details_on_blog_details_page(self):
        responce = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(responce, self.post1.title)
        self.assertContains(responce, self.post1.text)

    def test_status_404_if_post_id_not_exist(self):
        responce = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(responce.status_code, 404)

    def test_draft_post_not_show_in_posts_list(self):
        responce = self.client.get(reverse('posts_list'))
        self.assertContains(responce, self.post1.title)
        self.assertNotContains(responce, self.post2.title)

    def test_post_create_view(self):
        responce = self.client.post(reverse('post_create'), {
            'title': 'Some Title',
            'text': 'This is some text!',
            'status': 'pub',
            'author': self.user.id,
        })
        self.assertEqual(responce.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Some Title')
        self.assertEqual(Post.objects.last().text, 'This is some text!')

    def test_post_update_view(self):
        responce=self.client.post(reverse('post_update',args=[self.post2.id]),{
            'title':'Post2 Updated',
            'text':'This text is updated',
            'status': 'pub',
            'author': self.post2.author.id,

        })
        self.assertEqual(responce.status_code, 302)
        self.assertEqual(Post.objects.last().title, 'Post2 Updated')
        self.assertEqual(Post.objects.last().text, 'This text is updated')

    def test_post_delete_veiw(self):
        responce = self.client.post(reverse('post_delete', args=[self.post2.id]),)
        self.assertEqual(responce.status_code, 302)
