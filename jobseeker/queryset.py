from django.db import models
from django.utils import timezone
from django.db.models import Q


class LowonganQuerySet(models.QuerySet):


    def _update_status_by_date(self):
        current_date = timezone.now().date()
        
        # update if already verified and in valid lowongan date

        self.filter(
            status='Sudah terverifikasi',
            buka_lowongan__lte=current_date,
            batas_pengumpulan__gte=current_date
        ).update(
            status='Buka'
        )

        # close lowongan regardless of current status if current_date already 

        self.filter(
            batas_pengumpulan__lt=current_date
        ).update(
            status='Tutup'
        )
    
    def all_open_lowongan(self):
        self._update_status_by_date()
        return self.filter(status='Buka')
    
    def search(self,search_query):
        return self.all_open_lowongan().filter(
                (
                    Q(posisi__icontains=search_query) |
                    Q(users_id__name__icontains=search_query)
                )
            )