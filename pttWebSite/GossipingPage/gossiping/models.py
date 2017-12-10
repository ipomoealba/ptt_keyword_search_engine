from __future__ import unicode_literals

from django.db import models


class BiSexual(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=100)
    ptime = models.DateTimeField()
    arthor = models.CharField(max_length=30)
    ip = models.CharField(max_length=16, blank=True, null=True)
    content_keywords = models.TextField(blank=True, null=True)
    comment_keywords = models.TextField(blank=True, null=True)
    push = models.IntegerField(blank=True, null=True)
    sheee = models.IntegerField(blank=True, null=True)
    arrow = models.IntegerField(blank=True, null=True)
    first_page = models.IntegerField()
    relink = models.IntegerField()
    board = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bi_sexual'


class BiSexualContent(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bi_sexual_Content'


class BiSexualReply(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    reply = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Bi_sexual_Reply'


class FeminineSex(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=100)
    ptime = models.DateTimeField()
    arthor = models.CharField(max_length=30)
    ip = models.CharField(max_length=16, blank=True, null=True)
    content_keywords = models.TextField(blank=True, null=True)
    comment_keywords = models.TextField(blank=True, null=True)
    push = models.IntegerField(blank=True, null=True)
    sheee = models.IntegerField(blank=True, null=True)
    arrow = models.IntegerField(blank=True, null=True)
    first_page = models.IntegerField()
    relink = models.IntegerField()
    board = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Feminine_Sex'


class FeminineSexContent(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Feminine_Sex_Content'


class FeminineSexReply(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    reply = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Feminine_Sex_Reply'


class Gay(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=100)
    ptime = models.DateTimeField()
    arthor = models.CharField(max_length=30)
    ip = models.CharField(max_length=16, blank=True, null=True)
    content_keywords = models.TextField(blank=True, null=True)
    comment_keywords = models.TextField(blank=True, null=True)
    push = models.IntegerField(blank=True, null=True)
    sheee = models.IntegerField(blank=True, null=True)
    arrow = models.IntegerField(blank=True, null=True)
    first_page = models.IntegerField()
    relink = models.IntegerField()
    board = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Gay'


class GayContent(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Gay_Content'


class GayReply(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    reply = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Gay_Reply'


class Gossiping(models.Model):
    pid = models.CharField(primary_key=True, max_length=30)
    title = models.CharField(max_length=100)
    ptime = models.DateTimeField()
    arthor = models.CharField(max_length=30)
    ip = models.CharField(max_length=16, blank=True, null=True)
    content_keywords = models.TextField(blank=True, null=True)
    comment_keywords = models.TextField(blank=True, null=True)
    push = models.IntegerField(blank=True, null=True)
    sheee = models.IntegerField(blank=True, null=True)
    arrow = models.IntegerField(blank=True, null=True)
    first_page = models.IntegerField()
    relink = models.IntegerField()
    board = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Gossiping'


class GossipingContent(models.Model):
    pid = models.CharField(primary_key=True, max_length=30)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Gossiping_Content'


class GossipingReply(models.Model):
    pid = models.CharField(primary_key=True, max_length=30)
    reply = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Gossiping_Reply'


class Keywords(models.Model):
    pid = models.CharField(primary_key=True, max_length=30)
    content_keywords = models.TextField(blank=True, null=True)
    comment_keywords = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Keywords'


class Newkeywords(models.Model):
    id = models.CharField(primary_key=True, max_length=40)
    date = models.DateTimeField()
    keyword = models.CharField(max_length=50)
    category = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'Newkeywords'


class Sex(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    title = models.CharField(max_length=100)
    ptime = models.DateTimeField()
    arthor = models.CharField(max_length=30)
    ip = models.CharField(max_length=16, blank=True, null=True)
    content_keywords = models.TextField(blank=True, null=True)
    comment_keywords = models.TextField(blank=True, null=True)
    push = models.IntegerField(blank=True, null=True)
    sheee = models.IntegerField(blank=True, null=True)
    arrow = models.IntegerField(blank=True, null=True)
    first_page = models.IntegerField()
    relink = models.IntegerField()
    board = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sex'


class SexContent(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    content = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sex_Content'


class SexReply(models.Model):
    pid = models.CharField(primary_key=True, max_length=32)
    reply = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sex_Reply'


class UserSavePost(models.Model):
    pid = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField(max_length=32)
    class_id = models.CharField(max_length=100)
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    post_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User_Save_Post'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
