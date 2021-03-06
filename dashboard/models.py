"""Define the data models for all Sawaliram content"""

import datetime
from django.db import models

LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('ta', 'Tamil'),
    ('te', 'Telugu')
]

LANGUAGE_CODES = {
    'english': 'en',
    'hindi': 'hi',
    'bengali': 'bn',
    'malayalam': 'ml',
    'marathi': 'mr',
    'tamil': 'ta',
    'telugu': 'te'
}


class Dataset(models.Model):
    """Define the data model for submitted datasets"""

    question_count = models.CharField(max_length=100)
    submitted_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='submitted_datasets',
        on_delete=models.PROTECT)
    status = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class QuestionArchive(models.Model):
    """Define the data model for raw submissions by volunteers"""

    class Meta:
        db_table = 'question_archive'

    school = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, default='', blank=True)
    student_name = models.CharField(max_length=100, blank=True)
    student_gender = models.CharField(max_length=100, default='', blank=True)
    student_class = models.CharField(max_length=100, default='', blank=True)
    question_text = models.CharField(max_length=1000, blank=True)
    question_text_english = models.CharField(max_length=1000, default='', blank=True)
    question_format = models.CharField(max_length=100, blank=True)
    question_language = models.CharField(max_length=100, blank=True)
    contributor = models.CharField(max_length=100, blank=True)
    contributor_role = models.CharField(max_length=100, blank=True)
    context = models.CharField(max_length=100, blank=True)
    medium_language = models.CharField(max_length=100, blank=True)
    curriculum_followed = models.CharField(max_length=100, default='', blank=True)
    published = models.BooleanField(default=False)
    published_source = models.CharField(max_length=200, default='', blank=True)
    published_date = models.DateField(default=datetime.date.today)
    question_asked_on = models.DateField(null=True)
    notes = models.CharField(max_length=1000, default='')
    submitted_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='archived_questions',
        on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def accept_question(self, acceptor):
        """
        Mark a question as approved, by the given acceptor (user).

        This basically changes a question from unmoderated to moderated
        by removing the QuestionArchive record and replacing it with
        a Question one.
        """

        q = Question()
        q.school = self.school
        q.area = self.area
        q.state = self.state
        q.student_name = self.student_name
        q.student_gender = self.student_gender
        q.student_class = self.student_class
        q.question_text = self.question_text
        q.question_text_english = self.question_text_english
        q.question_format = self.question_format
        q.question_language = self.question_language
        q.contributor = self.contributor
        q.contributor_role = self.contributor_role
        q.context = self.context
        q.medium_language = self.medium_language
        q.curriculum_followed = self.curriculum_followed
        q.published = self.published
        q.published_source = self.published_source
        q.published_date = self.published_date
        q.question_asked_on = self.question_asked_on
        q.notes = self.notes
        q.created_on = self.created_on
        q.updated_on = self.updated_on
        q.submitted_by = self.submitted_by
        q.curated_by = acceptor
        try:
            q.save()
            self.delete()
        except Exception as e:
            print('Error accepting question: %s' % e)

    def __str__(self):
        return self.question_text


class Question(models.Model):
    """Define the data model for questions curated by admins."""

    class Meta:
        db_table = 'question'

    school = models.CharField(max_length=100, blank=True)
    area = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, default='', blank=True)
    student_name = models.CharField(max_length=100, blank=True)
    student_gender = models.CharField(max_length=100, default='', blank=True)
    student_class = models.CharField(max_length=100, default='', blank=True)
    question_text = models.CharField(max_length=1000, blank=True)
    question_text_english = models.CharField(max_length=1000, default='', blank=True)
    question_format = models.CharField(max_length=100, blank=True)
    question_language = models.CharField(max_length=100, blank=True)
    contributor = models.CharField(max_length=100, blank=True)
    contributor_role = models.CharField(max_length=100, blank=True)
    context = models.CharField(max_length=100, blank=True)
    medium_language = models.CharField(max_length=100, blank=True)
    curriculum_followed = models.CharField(max_length=100, default='', blank=True)
    published = models.BooleanField(default=False)
    published_source = models.CharField(max_length=200, default='', blank=True)
    published_date = models.DateField(default=datetime.date.today)
    question_asked_on = models.DateField(null=True)
    notes = models.CharField(max_length=1000, default='', blank=True)
    dataset_id = models.CharField(max_length=100, default='', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    curated_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='curated_questions',
        on_delete=models.PROTECT,
        default='')
    encoded_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='encoded_questions',
        on_delete=models.PROTECT,
        default='',
        blank=True,
        null=True)
    # data members for encoding
    field_of_interest = models.CharField(max_length=100, default='', blank=True)
    subject_of_session = models.CharField(max_length=100, default='', blank=True)
    question_topic_relation = models.CharField(max_length=100, default='', blank=True)
    motivation = models.CharField(max_length=100, default='', blank=True)
    type_of_information = models.CharField(max_length=100, default='', blank=True)
    source = models.CharField(max_length=100, default='', blank=True)
    curiosity_index = models.CharField(max_length=100, default='', blank=True)
    urban_or_rural = models.CharField(max_length=100, default='', blank=True)
    type_of_school = models.CharField(max_length=100, default='', blank=True)
    comments_on_coding_rationale = models.CharField(max_length=500, default='', blank=True)

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    """Define the data model for answers in English"""

    class Meta:
        db_table = 'answer'

    answer_text = models.TextField()
    language = models.CharField(
        max_length=100,
        default='en')
    question_id = models.ForeignKey(
        'Question',
        related_name='answers',
        on_delete=models.PROTECT,
        default='')
    status = models.CharField(max_length=50, default='submitted')
    submitted_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='answers',
        on_delete=models.PROTECT,
        default='')
    approved_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='approved_answers',
        on_delete=models.PROTECT,
        default='',
        null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        '''Return unicode representation of this Answer'''

        return 'Answer [{}]: {}'.format(
            self.question_id.question_language,
            self.question_id.question_text,
        )

    def get_language_name(self):
        """
        Return the full language name
        """
        for language, code in LANGUAGE_CODES.items():
            if code == self.language:
                return language


class AnswerComment(models.Model):
    """Define the data model for comments on Answers"""

    class Meta:
        db_table = 'answer_comment'

    text = models.TextField()
    answer = models.ForeignKey(
        'Answer',
        related_name='comments',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='answer_comments',
        on_delete=models.PROTECT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class AnswerCredit(models.Model):
    """Define the data model for answer and article credits"""

    class Meta:
        db_table = 'answer_credit'
        ordering = ['id']

    credit_title = models.CharField(max_length=50)
    credit_user_name = models.CharField(max_length=50)
    is_user = models.BooleanField(default=False)
    user = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='answer_credits',
        on_delete=models.PROTECT,
        default='',
        null=True)
    answer = models.ForeignKey(
        'Answer',
        related_name='credits',
        on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class UncuratedSubmission(models.Model):
    """Define the data model to store submissions pending for curation"""

    class Meta:
        db_table = 'uncurated_submission'

    submission_method = models.CharField(max_length=50)
    submission_id = models.IntegerField()
    number_of_questions = models.IntegerField()
    excel_sheet_name = models.CharField(max_length=100)
    submitted_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='submissions',
        on_delete=models.PROTECT,
        default='')
    curated = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class UnencodedSubmission(models.Model):
    """Define the data model to store submissions pending for encoding"""

    class Meta:
        db_table = 'unencoded_submission'

    submission_id = models.IntegerField(null=True)
    number_of_questions = models.IntegerField()
    excel_sheet_name = models.CharField(max_length=100)
    encoded = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


class TranslatedQuestion(models.Model):
    """Define the data model to store translated questions"""

    class Meta:
        db_table = 'translated_question'

    question_id = models.ForeignKey(
        'Question',
        related_name='translations',
        on_delete=models.PROTECT,
        default='')
    question_text = models.CharField(max_length=1000)
    language = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

class PublishedArticleManager(models.Manager):
    def get_queryset(self):
        return (super()
            .get_queryset()
            .filter(status=Article.STATUS_PUBLISHED))

class ArticleDraftManager(models.Manager):
    def get_queryset(self):
        return (super()
            .get_queryset()
            .filter(status=Article.STATUS_DRAFT))

class SubmittedArticleManager(models.Manager):
    def get_queryset(self):
        return (super()
            .get_queryset()
            .filter(status=Article.STATUS_SUBMITTED))

class Article(models.Model):
    '''
    Complete data model holding all kinds of articles. This includes:
      * ArticleDraft
      * SubmittedArticle
      * Article

    This is internally tracked via the 'status' parameter. You can
    also query articles with the specified status by using its proxy
    model (which internally checks the 'status' prameter before
    returning results).
    '''

    STATUS_DRAFT = -1
    STATUS_SUBMITTED = 0
    STATUS_PUBLISHED = 1

    title = models.CharField(max_length=1000, null=True)
    language = models.CharField(max_length=100,
        choices=LANGUAGE_CHOICES,
        default='en')
    author = models.ForeignKey('sawaliram_auth.User',
        related_name='articles',
        on_delete=models.PROTECT,
        default='',
        null=True)

    body = models.TextField(null=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    approved_by = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='approved_articles',
        on_delete=models.PROTECT,
        default='',
        null=True)
    published_on = models.DateTimeField(auto_now_add=True)

    status = models.IntegerField(default=-1) # draft

    get_published = PublishedArticleManager()
    get_drafts = ArticleDraftManager()
    get_submitted = SubmittedArticleManager()

    @property
    def is_draft(self):
        return self.status == self.STATUS_DRAFT

    @property
    def is_submitted(self):
        return self.status == self.STATUS_SUBMITTED

    @property
    def is_published(self):
        return self.status == self.STATUS_PUBLISHED

    class Meta:
        db_table = 'articles'

class ArticleDraft(Article):
    '''
    Draft articles are visible only to the user who creates them.
    Once ready, they can be submitted by converting to a
    SubmittedArticle which, upon approval, will be finally released
    to the world as a published Article.

    The complete sequence is:
        ArticleDraft -> SubmittedArticle -> Article
    '''

    class Meta:
        db_table = 'articles'
        proxy=True

    objects = ArticleDraftManager()

    def __init__(self, *args, **kwargs):
        self._meta.get_field('status').default = self.STATUS_DRAFT
        super().__init__(*args, **kwargs)

    def submit_draft(self):
        '''
        Submit the draft. In other words, copy over content to a new
        SubmittedArticle object and destroy self.
        '''

        try:
            self.status = self.STATUS_SUBMITTED
            self.save()
        except Exception as e:
            error = 'Error submitting article: %s' % e
            print(error)
            raise e

        return SubmittedArticle.objects.get(pk=self.pk)

class SubmittedArticle(Article):
    '''
    Submitted articles are article which are ready to publish, but which
    have to be vetted by an editor or manager before they are released
    to the world as a published Article

    The complete sequence is:
        ArticleDraft -> SubmittedArticle -> Article
    '''

    class Meta:
        db_table = 'articles'
        proxy=True

    objects = SubmittedArticleManager()

    def __init__(self, *args, **kwargs):
        self._meta.get_field('status').default = self.STATUS_SUBMITTED
        super().__init__(*args, **kwargs)

    def publish(self, approved_by):
        '''
        Publish the article. In other words, copy over content to a new
        Article object and destroy self.
        '''

        try:
            self.approved_by = approved_by
            self.status = self.STATUS_PUBLISHED
            self.save()
        except Exception as e:
            error = 'Error publishing article: %s' % e
            print(error)
            raise e

        return Article(self)

class PublishedArticle(Article):
    '''
    Articles are published articles, visible to the world after having
    gone through the full editorial process

    The complete sequence is:
        ArticleDraft -> SubmittedArticle -> PublishedArticle
    '''

    class Meta:
        db_table = 'articles'
        proxy = True

    objects = PublishedArticleManager()

    def __init__(self, *args, **kwargs):
        self._meta.get_field('status').default = self.STATUS_PUBLISHED
        super().__init__(*args, **kwargs)
class ArticleComment(models.Model):
    """Define the data model for comments on Answers"""

    class Meta:
        db_table = 'article_comment'

    text = models.TextField()

    article = models.ForeignKey(
        'Article',
        related_name='comments',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        'sawaliram_auth.User',
        related_name='article_comments',
        on_delete=models.PROTECT)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
