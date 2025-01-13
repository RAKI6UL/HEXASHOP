from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.exceptions import ValidationError

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_seller = models.BooleanField(default=False)
    user_profile_picture = models.ImageField(
        upload_to='photos/user_profile_picture', null=True, blank=True
    )

    objects = CustomUserManager()

    def delete(self, *args, **kwargs):
        """
        Prevent deletion of superuser accounts. Handle related objects before deletion to avoid IntegrityError.
        """
   #     if self.is_superuser:
    #        raise ValidationError("Superuser accounts cannot be deleted.")
        
        # Handle related objects before deletion to avoid integrity error
        self._cleanup_related_objects()
        super().delete(*args, **kwargs)

    def _cleanup_related_objects(self):
        """
        Clean up related objects like Ratings, Comments, or CartItems if they exist.
        If using `on_delete=models.SET_NULL`, we don't need to delete these objects but set the related field to NULL.
        """
        if hasattr(self, 'ratings'):
            self.ratings.update(user=None)  # Set user to NULL if you don't want to delete ratings
        if hasattr(self, 'comments'):
            self.comments.update(user=None)  # Set user to NULL if you don't want to delete comments
        if hasattr(self, 'cart_items'):
            self.cart_items.update(user=None)  # Set user to NULL if you don't want to delete cart items

    def __str__(self):
        return self.username
