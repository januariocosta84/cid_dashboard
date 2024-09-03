from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
class Position(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self) -> str:
        return self.name

class Agency(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    modify_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        self.modify_at = timezone.now()
        super(Agency, self).save(*args, **kwargs)

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, position, agency, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            position=position,
            agency=agency,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, position, agency, password=None):
        user = self.create_user(
            username,
            email,
            first_name,
            last_name,
            position,
            agency,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True)
    agency = models.ForeignKey(Agency, on_delete=models.SET_NULL, null=True)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'position', 'agency']

    objects = CustomUserManager()

    class Meta:
        db_table = 'custom_auth_user'

    def __str__(self):
        return self.username

class Audits(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    action = models.CharField(max_length=200)
    activity = models.TextField()
    entity = models.CharField(max_length=200, blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'audits'

class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        db_table = 'auth_group'

class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)
    permission = models.ForeignKey('AuthPermission', on_delete=models.CASCADE)

    class Meta:
        db_table = 'cidapp_auth_group_permissions'
        unique_together = (('group', 'permission'),)

class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.CASCADE)
    codename = models.CharField(max_length=100)

    class Meta:
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)

class AuthUserGroups(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    group = models.ForeignKey(AuthGroup, on_delete=models.CASCADE)

    class Meta:
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)

class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, on_delete=models.CASCADE)

    class Meta:
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)

class Comments(models.Model):
    record = models.ForeignKey('Records', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comments'

class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    class Meta:
        db_table = 'django_admin_log'

class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)

class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        db_table = 'django_migrations'

class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        db_table = 'django_session'

class Files(models.Model):
    path = models.CharField(max_length=200)
    size = models.IntegerField()
    mimetype = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=500)

    class Meta:
        db_table = 'files'

class Records(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    department = models.ForeignKey('References', on_delete=models.CASCADE, blank=True, null=True)
    information_source = models.ForeignKey('References', on_delete=models.CASCADE, related_name='records_information_source_set')
    subject = models.ForeignKey('Subjects', on_delete=models.CASCADE, blank=True, null=True)
    records_source = models.ForeignKey('RecordsSource', on_delete=models.CASCADE, blank=True, null=True)
    information_source_other = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('References', on_delete=models.CASCADE, related_name='records_status_set')

    class Meta:
        db_table = 'records'

class RecordsFiles(models.Model):
    record = models.ForeignKey(Records, on_delete=models.CASCADE)
    file = models.ForeignKey(Files, on_delete=models.CASCADE)

    class Meta:
        db_table = 'records_files'

class RecordsRequest(models.Model):
    record = models.ForeignKey(Records, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    agency = models.ForeignKey('References', on_delete=models.CASCADE)
    status = models.ForeignKey('References', on_delete=models.CASCADE, related_name='recordsrequest_status_set')
    name = models.CharField(max_length=300, blank=True, null=True)
    position = models.CharField(max_length=300, blank=True, null=True)
    other = models.CharField(max_length=300, blank=True, null=True)
    email_addresses = models.CharField(max_length=300, blank=True, null=True)
    justification = models.TextField(blank=True, null=True)
    legal_provision = models.IntegerField(blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    handling_code = models.ForeignKey('References', on_delete=models.CASCADE, related_name='recordsrequest_handling_code_set', blank=True, null=True)
    justification_review = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'records_request'

class RecordsReviewed(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    record = models.ForeignKey(Records, on_delete=models.CASCADE)
    section = models.ForeignKey('References', on_delete=models.CASCADE)
    status = models.ForeignKey('References', on_delete=models.CASCADE, related_name='recordsreviewed_status_set')
    handling_code = models.ForeignKey('References', on_delete=models.CASCADE, related_name='recordsreviewed_handling_code_set', blank=True, null=True)
    justification_review = models.TextField(blank=True, null=True)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'records_reviewed'

class References(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    code = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'references'

class Sessions(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        db_table = 'sessions'

class Subjects(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'subjects'

class RecordsSource(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'records_source'
