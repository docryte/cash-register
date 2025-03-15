from django.template.loader import render_to_string
from .base import HTMLServiceInterface
from typing import Any, Dict


class DjangoHTMLRenderer(HTMLServiceInterface):
    """
    Сервис для рендеринга HTML с использованием Django шаблонов.
    """

    def render_to_string(self, template_name: str, context: Dict[str, Any]) -> str:
        """
        Рендерит HTML шаблон с контекстом.

        Args:
            template_name: Имя шаблона
            context: Контекст для шаблона

        Returns:
            str: Отрендеренный HTML

        Raises:
            TemplateDoesNotExist: Если шаблон не найден
            TemplateSyntaxError: Если в шаблоне есть синтаксические ошибки
        """
        return render_to_string(template_name, context)
