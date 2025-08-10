from django.db import models


class USER_ROLE(models.TextChoices):
    ADMIN = 'admin'
    ORGANIZATION_ADMIN = 'organization_admin'
    SHOP_ADMIN = 'shop_admin'
  
    USER = 'user'


class ORDER_STATUS(models.TextChoices):
        PENDING ='pending'
        PROCESSING = 'processing'
        READY = 'ready'
        COMPLETED ='completed'
        CANCLED ='cancled'

class MESSAGE_SENDER(models.TextChoices):
      USER='user'
      SYSTEM = 'system'