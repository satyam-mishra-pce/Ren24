from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations=True

    def create_user(self,phone=None,email=None,password=None,**extra):
        if not phone:
            raise ValueError('Phone is required')
        if len(phone) != 10:
            raise ValueError('Invalid Phone Number')
        if not email:
            email=""
        # email = self.normalize_email(email)
        user = self.model(phone=phone,email=email,**extra)
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self,phone,password,**extra):
        extra.setdefault('is_staff',True)
        extra.setdefault('is_superuser',True)
        extra.setdefault('is_active',True)

        if extra.get('is_staff') is not True:
            raise ValueError(('is_staff should be True for Superuser'))

        return self.create_user(phone=phone,password=password,**extra) 