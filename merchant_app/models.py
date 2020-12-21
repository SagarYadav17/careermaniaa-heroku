from django.db import models


# Create your models here.


class Merchant_Details(models.Model):
    merchant = models.ForeignKey('mania.User', on_delete=models.CASCADE)
    merchant_type = models.CharField(max_length=10, default=None)
    first_name = models.CharField(max_length=250, blank=False, null=False)
    last_name = models.CharField(max_length=250, blank=False, null=False)
    email = models.CharField(max_length=250, blank=False, null=False)
    mobile = models.CharField(max_length=250, blank=False, null=False)
    stream = models.CharField(max_length=250, blank=False, null=False,
                              verbose_name='coaching_stream', default=None
                              )

    def __str__(self):
        return self.first_name + " " + self.last_name


class Coaching(models.Model):
    merchant = models.OneToOneField('mania.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=250, unique=True,
                            blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    logo = models.ImageField(upload_to='logos/', default=None)

    def __str__(self):
        return self.name


class BankAccountDetails(models.Model):
    coaching = models.OneToOneField(Coaching, on_delete=models.CASCADE)
    account_no = models.CharField(max_length=30, default=None)
    ifsc_code = models.CharField(max_length=20, default=None)
    bank_name = models.CharField(max_length=50, default=None)
    account_holder = models.CharField(max_length=100, default=None)
    adhar_card = models.FileField(
        upload_to="adhar_cards/", default=None)
    pan_card = models.FileField(upload_to="pan_cards/", default=None)
    mobile_no = models.CharField(max_length=20, default=None)

    def __str__(self):
        return self.coaching.name


class CoachingFacultyMember(models.Model):
    coaching = models.ForeignKey(
        Coaching, related_name="faculty_of", on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False, null=False)
    age = models.PositiveIntegerField()
    specialization = models.CharField(max_length=250, blank=False, null=False)
    faculty_image = models.ImageField(
        upload_to='faculties/', default=None)

    def __str__(self):
        return self.name


class CoachingReview(models.Model):
    coaching = models.ForeignKey(
        Coaching, related_name='reviews_of', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    description = models.CharField(max_length=250, default=None)


class Branch(models.Model):
    name = models.CharField(max_length=250, blank=False,
                            null=False, verbose_name='coaching_branch_name')
    coaching = models.ForeignKey(
        Coaching, related_name='branches', on_delete=models.CASCADE)
    branch_type = models.CharField(max_length=250, blank=False, null=False,
                                   verbose_name='coaching_branch', default="Main"
                                   )

    def __str__(self):
        return self.name


class Geolocation(models.Model):
    address = models.OneToOneField(
        'mania.Address', related_name='location_of', on_delete=models.CASCADE)
    lat = models.DecimalField(
        decimal_places=2, max_digits=10, null=False, default=None)
    lng = models.DecimalField(
        decimal_places=2, max_digits=10, null=False, default=None)

    def __str__(self):
        return str(self.address)


class Course(models.Model):
    name = models.CharField(max_length=250, blank=False,
                            null=False, verbose_name='branch_course_name')
    coaching = models.ForeignKey(Coaching, on_delete=models.CASCADE)
    timePeriod = models.CharField(max_length=20, default=None)
    trial = models.CharField(default='Not Available', max_length=10)
    branch = models.ForeignKey(
        Branch, related_name='courses_of', on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    syllabus = models.FileField(blank=True, null=True)
    fees = models.DecimalField(
        blank=False, null=False, max_digits=10, decimal_places=2, default=None)
    currency = models.CharField(
        max_length=30, blank=True, null=False, default="INR")
    is_active = models.BooleanField(default=False)
    stream = models.CharField(max_length=250, blank=False, null=False,
                              verbose_name='coaching_stream', default=None
                              )

    def __str__(self):
        return self.name


class CoachingMetaData(models.Model):
    coaching = models.ForeignKey(
        Coaching, related_name="metadata_of", on_delete=models.CASCADE)
    owner_name = models.CharField(max_length=250, default=None)
    owner_image = models.ImageField(upload_to='owners/', default=None)
    established_on = models.DateField()
    mobile = models.PositiveIntegerField()

    def __str__(self):
        return self.coaching.name


class Batch(models.Model):
    name = models.CharField(max_length=250, blank=False,
                            null=False, verbose_name='course_batch_name')
    course = models.ForeignKey(
        Course, related_name='batches_of', on_delete=models.CASCADE)
    teacher = models.ForeignKey(CoachingFacultyMember, related_name='teaches',
                                on_delete=models.CASCADE, null=False, blank=False)
    start_time = models.CharField(max_length=20, default=None)
    end_time = models.CharField(max_length=20, default=None)
    student_limit = models.PositiveIntegerField(blank=True, null=True)
    students_enrolled = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Offer(models.Model):
    name = models.CharField(max_length=100, default=None)
    description = models.CharField(max_length=200, default=None)
    coaching = models.ForeignKey(Coaching, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Discount(models.Model):
    coaching = models.ForeignKey(Coaching, on_delete=models.CASCADE)
    disc_code = models.CharField(max_length=20, default=None)
    description = models.CharField(max_length=200, default=None)
    disc_percent = models.IntegerField(default=None)

    def __str__(self):
        return self.disc_code


class Review(models.Model):
    reviewer = models.ForeignKey('mania.User', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default=None)
    rating = models.IntegerField(default=None)
    coaching = models.ForeignKey(Coaching, on_delete=models.CASCADE)
    review_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.coaching.name + " - Review By : " + self.user.username


class Message(models.Model):
    message = models.CharField(max_length=200, default=None)
    sender = models.ForeignKey(
        'mania.User', on_delete=models.CASCADE, related_name="msg_sender")
    receiver = models.ForeignKey(
        'mania.User', on_delete=models.CASCADE, related_name="msg_receiver")
    timestamp = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return str(self.sender) + " - Message : " + self.message


class College(models.Model):
    user = models.OneToOneField('mania.User', on_delete=models.CASCADE)
    registration_no = models.SmallIntegerField()
    contact_no = models.PositiveIntegerField()
    college_name = models.CharField(max_length=255, default=None)
    university_type = models.CharField(max_length=50, default=None)
    institute_type = models.CharField(max_length=50, default=None)
    chairman = models.CharField(max_length=50, default=None)
    college_address = models.CharField(max_length=255, default=None)
    country = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=50, default=None)
    city = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.college_name


class Booking(models.Model):
    BOOKING_STATUS = (
        ('Pending for Approval', 'Pending for Approval'),
        ('Awaiting', 'Awaiting'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    user = models.ForeignKey('mania.User', on_delete=models.CASCADE)
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField()
    status = models.CharField(choices=BOOKING_STATUS,
                              max_length=20, default=None)

    def __str__(self):
        return self.user


class Job(models.Model):
    user = models.ForeignKey('mania.User', on_delete=models.CASCADE)
    contact_no = models.PositiveIntegerField()
    registration_no = models.CharField(max_length=50, default=None)
    company_name = models.CharField(max_length=100, default=None)
    company_address = models.CharField(max_length=500, default=None)
    city = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=50, default=None)
    country = models.CharField(max_length=50, default=None)
    director_name = models.CharField(max_length=50, default=None)
    industry_type = models.CharField(max_length=50, default=None)

    def __str__(self):
        return self.company_name
