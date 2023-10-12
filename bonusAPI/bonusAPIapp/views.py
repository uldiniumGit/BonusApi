from .models import Roulette
from django.http import JsonResponse
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from random import choices
from rest_framework.response import Response


class RandomBonusView(APIView):
    def get_bonus(self, request):
        # Получаем unique_id из запроса
        unique_id = request.GET.get('unique_id')

        # Получаем объект Roulette по unique_id
        roulette = get_object_or_404(Roulette, unique_id=unique_id)

        # Получаем все бонусы для данного объекта Roulette
        bonuses = roulette.bonuses.all()

        # Определите количество бонусов и их вероятности
        bonus_counts = [1, 2, 3]
        probabilities = [0.5, 0.3, 0.2]

        # Выберите количество бонусов с учетом вероятностей
        num_bonuses = choices(bonus_counts, probabilities)[0]

        # Получаем словарь, где каждому типу бонуса соответствует список всех бонусов этого типа
        bonus_types = {}
        for bonus in bonuses:
            if bonus.type not in bonus_types:
                bonus_types[bonus.type] = []
            bonus_types[bonus.type].append(bonus)

        # Выбираем случайный тип бонусов для каждого бонуса
        selected_bonuses = []
        for i in range(num_bonuses):
            if not bonus_types:  # Если все типы бонусов уже использованы, прерываем цикл
                break

            # Выбираем случайный тип бонуса в соответствии с вероятностью
            type_probabilities = [bonus_type.probability for bonus_type in bonus_types.keys()]
            bonus_type = choices(list(bonus_types.keys()), type_probabilities)[0]

            # Выбираем случайный бонус для данного типа в соответствии с вероятностью
            probabilities = [bonus.probability for bonus in bonus_types[bonus_type]]
            selected_bonus = choices(bonus_types[bonus_type], probabilities)[0]

            selected_bonuses.append(selected_bonus)

            # Удаляем выбранный тип бонуса из списка доступных типов
            del bonus_types[bonus_type]

        # Возвращаем словарь с выпавшими бонусами
        return {bonus.name: {'value': bonus.value, 'type': bonus.type.type, 'probability': bonus.probability} for bonus
                in selected_bonuses}

    def get(self, request):
        bonuses = self.get_bonus(request)
        request.session['bonuses'] = ({bonus: data['value'] for bonus, data in bonuses.items()})
        request.session.save()
        return JsonResponse({bonus: data['value'] for bonus, data in bonuses.items()})

    def post(self, request):
        bonuses = request.session.get('bonuses', {})
        name = request.GET.get('name')
        phone = request.GET.get('phone')
        email = request.GET.get('email')
        print(bonuses, name, phone, email)

        return Response({"message": "Успешно!"})
