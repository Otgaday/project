from rest_framework import generics
from resource_accounting.serializers import ResourceDetailSerializer
from resource_accounting.models import Resource_accounting
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from django.db.models import  Count
import numpy as np

# прописываем отображения

class Update_delete_resources(generics.RetrieveUpdateDestroyAPIView):
    # берем сет данных (аналог запроса)
    queryset = Resource_accounting.objects.all()
    #Сериализуем
    serializer_class = ResourceDetailSerializer
    renderer_classes = [JSONRenderer]


# Т.к. в задании нет исходного значения стоимости "cost", необходимо произвести его расчет
# Также в исходной бд условие: цена за единицу имеет строковый тип данных. Необходимо преобразовать
class Create_resource(generics.ListCreateAPIView):
    queryset = Resource_accounting.objects.all()
    serializer_class = ResourceDetailSerializer
    renderer_classes = [JSONRenderer]

    def get(self, request):
        buf = []
        to_ret = []
        transaction = Resource_accounting.objects.all()
        serializer = ResourceDetailSerializer(transaction, many=True)
        transaction_1 = Resource_accounting.objects.values_list('price', flat=True)
        transaction_2 = Resource_accounting.objects.values_list('amount', flat=True)

        # перевод в числовой тип
        prices_float = list(map(float, (list(transaction_1))))
        amounts = list(transaction_2)
        cost = np.array(prices_float) * np.array(amounts)
        for b in cost.tolist():
            buf.append({"cost": b})

        sd = list(serializer.data)

        # для вывода складываем все в один словарь
        for i in range(len(sd)):
            to_ret.append({**serializer.data[i], **buf[i]})
        # операция агрегации
        all_count = transaction.aggregate(Count('title'))['title__count']

        # Выводим json
        return Response({'resources': to_ret, 'total_count': all_count if all_count else 0})


class Total_cost(GenericAPIView):
    renderer_classes = [JSONRenderer]
    def get(self, request):
        transaction_1 = Resource_accounting.objects.values_list('price', flat=True)
        transaction_2 = Resource_accounting.objects.values_list('amount', flat=True)
        prices_float = list(map(float, (list(transaction_1))))
        amounts = list(transaction_2)
        cost = np.array(prices_float) * np.array(amounts)
        return_data = {"total_cost": np.sum(cost)}

        return Response(return_data)