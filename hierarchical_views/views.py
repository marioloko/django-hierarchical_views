from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import ContextMixin

from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Create your views here.
class HierarchicalMixin(ContextMixin):
    model = None
    queryset = None
    pk_url_kwargs = None
    relation_names = None

    def get_pk_url_kwargs(self):
        if not self.pk_url_kwargs:
            raise ImproperlyConfigured(
                "{cls} is missing relation names. Define "
                "{cls}.relation_names in the order that "
                "they are referred in their child model "
                "appear on the URL.".format(
                    cls = self.__class__.__name__
                )
            )
        return self.pk_url_kwargs
        

    def get_relation_names(self):
        if not self.relation_names:
            raise ImproperlyConfigured(
                "{cls} is missing relation names. Define "
                "{cls}.relation_names in the order that "
                "they are referred in their child model "
                "appear on the URL, or override "
                "{cls}.get_relation_names().".format(
                    cls = self.__class__.__name__
                )
            )

        joined_list = []
        cumulative_relation = ""
        for relation_name in reversed(self.relation_names):
            cumulative_relation += ("__" + relation_name if cumulative_relation
                                                         else relation_name)
            joined_list.append(cumulative_relation)

        joined_list.reverse()
        return joined_list

    def get_queryset(self): 
        if self.queryset:
            return self.queryset

        if not self.model:
            raise ImproperlyConfigured(
                "{cls} is missing a QuerySet. Define "
                "{cls}.model{cls}, {cls}.queryset, or "
                "override {cls}.get_queryset".format(
                    cls = self.__class__.__name__
                )
            )

        pk_url_kwargs = self.get_pk_url_kwargs()

        relation_names = self.get_relation_names()
        relation_values = map(lambda pk: self.kwargs.get(pk), pk_url_kwargs)

        filters = dict(zip(relation_names, relation_values))

        return self.model._default_manager.filter(**filters)

class HierarchicalListView(HierarchicalMixin, ListView):
    pass

class HierarchicalDetailView(HierarchicalMixin, DetailView):
    pass

class HierarchicalCreateView(HierarchicalMixin, CreateView):
    pass

class HierarchicalUpdateView(HierarchicalMixin, UpdateView):
    pass

class HierarchicalDeleteView(HierarchicalMixin, DeleteView):
    pass
