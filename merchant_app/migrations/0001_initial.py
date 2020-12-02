from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('mania', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='coaching_branch_name')),
                ('branch_type', models.CharField(default='Main', max_length=250, verbose_name='coaching_branch')),
            ],
        ),
        migrations.CreateModel(
            name='Coaching',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, unique=True)),
                ('description', models.TextField()),
                ('logo', models.ImageField(blank=True, null=True, upload_to='logos/')),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(default=None, max_length=200)),
                ('rating', models.IntegerField(default=None)),
                ('review_time', models.DateTimeField(auto_now_add=True)),
                ('coaching', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant_app.Coaching')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=100)),
                ('description', models.CharField(default=None, max_length=200)),
                ('coaching', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant_app.Coaching')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(default=None, max_length=200)),
                ('timestamp', models.DateTimeField()),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='msg_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant_Details',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_type', models.CharField(blank=True, max_length=10, null=True)),
                ('first_name', models.CharField(max_length=250)),
                ('last_name', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('mobile', models.CharField(max_length=250)),
                ('stream', models.CharField(default=None, max_length=250, verbose_name='coaching_stream')),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_no', models.PositiveIntegerField()),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('company_address', models.CharField(blank=True, max_length=500, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Geolocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.DecimalField(decimal_places=2, default=None, max_digits=10)),
                ('lng', models.DecimalField(decimal_places=2, default=None, max_digits=10)),
                ('address', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='location_of', to='mania.Address')),
            ],
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('disc_code', models.CharField(default=None, max_length=20)),
                ('description', models.CharField(default=None, max_length=200)),
                ('disc_percent', models.IntegerField(default=None)),
                ('coaching', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant_app.Coaching')),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='branch_course_name')),
                ('timePeriod', models.CharField(blank=True, max_length=20, null=True)),
                ('trial', models.CharField(default='Not Available', max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('syllabus', models.FileField(blank=True, null=True, upload_to='')),
                ('fees', models.DecimalField(decimal_places=2, default=None, max_digits=10)),
                ('currency', models.CharField(blank=True, default='INR', max_length=30)),
                ('is_active', models.BooleanField(default=False)),
                ('stream', models.CharField(default=None, max_length=250, verbose_name='coaching_stream')),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_of', to='merchant_app.Branch')),
                ('coaching', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchant_app.Coaching')),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('registration_no', models.SmallIntegerField()),
                ('contact_no', models.PositiveIntegerField()),
                ('college_name', models.CharField(blank=True, max_length=255, null=True)),
                ('university_type', models.CharField(blank=True, max_length=50, null=True)),
                ('institute_type', models.CharField(blank=True, max_length=50, null=True)),
                ('chairman', models.CharField(blank=True, max_length=50, null=True)),
                ('college_address', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CoachingReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('coaching', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_of', to='merchant_app.Coaching')),
            ],
        ),
        migrations.CreateModel(
            name='CoachingMetaData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_name', models.CharField(blank=True, max_length=250, null=True)),
                ('owner_image', models.ImageField(blank=True, null=True, upload_to='owners/')),
                ('established_on', models.DateField()),
                ('mobile', models.PositiveIntegerField()),
                ('coaching', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metadata_of', to='merchant_app.Coaching')),
            ],
        ),
        migrations.CreateModel(
            name='CoachingFacultyMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('age', models.PositiveIntegerField()),
                ('specialization', models.CharField(max_length=250)),
                ('faculty_image', models.ImageField(blank=True, null=True, upload_to='faculties/')),
                ('coaching', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faculty_of', to='merchant_app.Coaching')),
            ],
        ),
        migrations.AddField(
            model_name='branch',
            name='coaching',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='merchant_app.Coaching'),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_in', models.DateTimeField(auto_now_add=True)),
                ('check_out', models.DateTimeField()),
                ('status', models.CharField(blank=True, choices=[('Pending for Approval', 'Pending for Approval'), ('Awaiting', 'Awaiting'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], max_length=20, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='course_batch_name')),
                ('start_time', models.CharField(default=None, max_length=20)),
                ('end_time', models.CharField(default=None, max_length=20)),
                ('student_limit', models.PositiveIntegerField(blank=True, null=True)),
                ('students_enrolled', models.PositiveIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='batches_of', to='merchant_app.Course')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teaches', to='merchant_app.CoachingFacultyMember')),
            ],
        ),
        migrations.CreateModel(
            name='BankAccountDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_no', models.CharField(default=None, max_length=30)),
                ('ifsc_code', models.CharField(default=None, max_length=20)),
                ('bank_name', models.CharField(default=None, max_length=50)),
                ('account_holder', models.CharField(default=None, max_length=100)),
                ('adhar_card', models.FileField(blank=True, null=True, upload_to='adhar_cards/')),
                ('pan_card', models.FileField(blank=True, null=True, upload_to='pan_cards/')),
                ('mobile_no', models.CharField(default=None, max_length=20)),
                ('coaching', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='merchant_app.Coaching')),
            ],
        ),
    ]
