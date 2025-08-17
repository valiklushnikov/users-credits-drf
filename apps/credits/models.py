from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Credits(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credits")
    issuance_date = models.DateField()
    return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    body = models.DecimalField(max_digits=12, decimal_places=2)
    percent = models.DecimalField(max_digits=12, decimal_places=2)


    class Meta:
        verbose_name = "Credits"
        verbose_name_plural = "Credits"

    def __str__(self):
        return str(
            f"User: {self.user.login} | Issue: {self.issuance_date} | "
            f"Return: {self.return_date} | Body: {self.body} | Percent: {self.percent}"
        )


class Dictionary(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name = "Dictionary"
        verbose_name_plural = "Dictionaries"

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


class Plans(models.Model):
    category = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name="plans")
    period = models.DateField()
    sum = models.IntegerField()

    class Meta:
        verbose_name = "Plan"
        verbose_name_plural = "Plans"

    def __str__(self):
        return str(f"{self.category} | {self.period} | {self.sum}")


class Payments(models.Model):
    sum = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField()
    credit = models.ForeignKey(Credits, on_delete=models.CASCADE, related_name="payments")
    type = models.ForeignKey(Dictionary, on_delete=models.CASCADE, related_name="payments")


    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return str(f"Sum: {self.sum} | Payment Date: {self.payment_date} | Credit: {self.credit} | Type: {self.type}")
