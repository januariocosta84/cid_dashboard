# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AdminTwoFactorTwofactorverification(models.Model):
    id = models.BigAutoField(primary_key=True)
    secret = models.CharField(unique=True, max_length=20, blank=True, null=True)
    code = models.CharField(max_length=8, blank=True, null=True)
    is_active = models.IntegerField()
    created_time = models.DateTimeField()
    updated_time = models.DateTimeField()
    user = models.OneToOneField('AuthUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'admin_two_factor_twofactorverification'


class Audits(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    action = models.CharField(max_length=200)
    activity = models.TextField()
    entity = models.CharField(max_length=200, blank=True, null=True)
    entity_id = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audits'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CidappAgency(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    modify_at = models.DateTimeField(blank=True, null=True)
    created_by_id = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'cidapp_agency'


class CidappProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    code = models.IntegerField(unique=True)
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    rating_rate = models.FloatField()
    rating_count = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'cidapp_product'


class Comments(models.Model):
    record = models.ForeignKey('Records', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    comment = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comments'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
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
    id = models.BigAutoField(primary_key=True)
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


class Files(models.Model):
    path = models.CharField(max_length=200)
    size = models.IntegerField()
    mimetype = models.CharField(max_length=200)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    name = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'files'


class OtpEmailEmaildevice(models.Model):
    name = models.CharField(max_length=64)
    confirmed = models.IntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    token = models.CharField(max_length=16, blank=True, null=True)
    valid_until = models.DateTimeField()
    email = models.CharField(max_length=254, blank=True, null=True)
    throttling_failure_count = models.PositiveIntegerField()
    throttling_failure_timestamp = models.DateTimeField(blank=True, null=True)
    last_generated_timestamp = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otp_email_emaildevice'


class OtpStaticStaticdevice(models.Model):
    name = models.CharField(max_length=64)
    confirmed = models.IntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    throttling_failure_count = models.PositiveIntegerField()
    throttling_failure_timestamp = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otp_static_staticdevice'


class OtpStaticStatictoken(models.Model):
    token = models.CharField(max_length=16)
    device = models.ForeignKey(OtpStaticStaticdevice, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'otp_static_statictoken'


class OtpTotpTotpdevice(models.Model):
    name = models.CharField(max_length=64)
    confirmed = models.IntegerField()
    key = models.CharField(max_length=80)
    step = models.PositiveSmallIntegerField()
    t0 = models.BigIntegerField()
    digits = models.PositiveSmallIntegerField()
    tolerance = models.PositiveSmallIntegerField()
    drift = models.SmallIntegerField()
    last_t = models.BigIntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    throttling_failure_count = models.PositiveIntegerField()
    throttling_failure_timestamp = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    last_used_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'otp_totp_totpdevice'


class Records(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    department = models.ForeignKey('References', models.DO_NOTHING, blank=True, null=True)
    information_source = models.ForeignKey('References', models.DO_NOTHING, related_name='records_information_source_set')
    subject = models.ForeignKey('Subjects', models.DO_NOTHING, blank=True, null=True)
    records_source = models.ForeignKey('RecordsSource', models.DO_NOTHING, blank=True, null=True)
    information_source_other = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    status = models.ForeignKey('References', models.DO_NOTHING, related_name='records_status_set')

    class Meta:
        managed = False
        db_table = 'records'


class RecordsFiles(models.Model):
    record = models.ForeignKey(Records, models.DO_NOTHING)
    file = models.ForeignKey(Files, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'records_files'


class RecordsRequest(models.Model):
    record = models.ForeignKey(Records, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    agency = models.ForeignKey('References', models.DO_NOTHING)
    status = models.ForeignKey('References', models.DO_NOTHING, related_name='recordsrequest_status_set')
    name = models.CharField(max_length=300, blank=True, null=True)
    position = models.CharField(max_length=300, blank=True, null=True)
    other = models.CharField(max_length=300, blank=True, null=True)
    email_addresses = models.CharField(max_length=300, blank=True, null=True)
    justification = models.TextField(blank=True, null=True)
    legal_provision = models.IntegerField(blank=True, null=True)
    number = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    handling_code = models.ForeignKey('References', models.DO_NOTHING, related_name='recordsrequest_handling_code_set', blank=True, null=True)
    justification_review = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records_request'


class RecordsReviewed(models.Model):
    user = models.ForeignKey('Users', models.DO_NOTHING)
    record = models.ForeignKey(Records, models.DO_NOTHING)
    section = models.ForeignKey('References', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records_reviewed'


class RecordsSource(models.Model):
    type = models.ForeignKey('References', models.DO_NOTHING)
    title = models.CharField(max_length=200)
    uri = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    entity_id = models.CharField(max_length=200, blank=True, null=True)
    processed = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records_source'


class RecordsStatus(models.Model):
    record = models.ForeignKey(Records, models.DO_NOTHING)
    status = models.ForeignKey('References', models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'records_status'


class References(models.Model):
    parent = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)
    ref_type = models.CharField(max_length=200)
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'references'


class RequestStatus(models.Model):
    request = models.ForeignKey(RecordsRequest, models.DO_NOTHING)
    status = models.ForeignKey(References, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'request_status'


class RolesPermissions(models.Model):
    role = models.ForeignKey(References, models.DO_NOTHING)
    permission = models.ForeignKey(References, models.DO_NOTHING, related_name='rolespermissions_permission_set')

    class Meta:
        managed = False
        db_table = 'roles_permissions'


class SourceMetadata(models.Model):
    records_source = models.ForeignKey(RecordsSource, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    value = models.TextField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    key = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'source_metadata'


class Subjects(models.Model):
    place_birth = models.ForeignKey(References, models.DO_NOTHING, blank=True, null=True)
    nationality = models.ForeignKey(References, models.DO_NOTHING, related_name='subjects_nationality_set', blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    gender = models.CharField(max_length=1, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    approx_age = models.IntegerField(blank=True, null=True)
    id_type = models.CharField(max_length=100, blank=True, null=True)
    id_number = models.CharField(max_length=100, blank=True, null=True)
    home_address = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    business_address = models.CharField(max_length=100, blank=True, null=True)
    bin_tin = models.CharField(max_length=100, blank=True, null=True)
    telephone = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    conveyance = models.ForeignKey(References, models.DO_NOTHING, related_name='subjects_conveyance_set', blank=True, null=True)
    conveyance_description = models.CharField(max_length=400, blank=True, null=True)
    status = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'subjects'


class Texts(models.Model):
    record = models.ForeignKey(Records, models.DO_NOTHING)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    text = models.TextField()
    information_source = models.ForeignKey(References, models.DO_NOTHING)
    source_evaluation = models.ForeignKey(References, models.DO_NOTHING, related_name='texts_source_evaluation_set')
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'texts'


class Users(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(unique=True, max_length=300)
    password_hash = models.CharField(max_length=300)
    is_active = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    failed_attempts = models.IntegerField(blank=True, null=True)
    last_failed = models.DateTimeField(blank=True, null=True)
    reset_token = models.CharField(max_length=200, blank=True, null=True)
    reset_created_at = models.DateTimeField(blank=True, null=True)
    mfa_secret = models.CharField(max_length=300, blank=True, null=True)
    mfa_active = models.IntegerField(blank=True, null=True)
    auth_mode = models.CharField(max_length=1, blank=True, null=True, db_comment='[P]ASSWORD, [M]FA')

    class Meta:
        managed = False
        db_table = 'users'


class UsersRoles(models.Model):
    reference = models.ForeignKey(References, models.DO_NOTHING)
    user = models.ForeignKey(Users, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_roles'
        unique_together = (('id', 'reference', 'user'),)
