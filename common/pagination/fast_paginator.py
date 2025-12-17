from django.core.paginator import Paginator

class FastPaginator(Paginator):
  def _get_count(self):
    if not hasattr(self, '_fast_count'):
      from common.pagination.get_fast_count import get_fast_count
      self._fast_count = get_fast_count(self.object_list.modele._meta.db_table)
    return self._fast_count

  count = property(_get_count)