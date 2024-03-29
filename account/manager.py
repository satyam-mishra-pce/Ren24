from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,email=None,password=None,**extra):
        print("Print here")
        if not email:
            raise ValueError('Email is required')
        # email = self.normalize_email(email)
        user = self.model(email=email,**extra)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self,email,password,**extra):
        extra.setdefault('is_staff',True)
        extra.setdefault('is_superuser',True)
        extra.setdefault('is_active',True)

        if extra.get('is_staff') is not True:
            raise ValueError(('is_staff should be True for Superuser'))

        return self.create_user(email=email,password=password,**extra) 