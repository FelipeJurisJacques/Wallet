from source.libraries.database.query import Query
from source.models.analyze import Analyze as AnalyzeModel
from source.enumerators.period import Period as PeriodEnum
from source.entities.analyze import Analyze as AnalyzeEntity
from source.models.prophesy import Prophesy as ProphesyModel
from source.enumerators.context import Context as ContextEnum
from source.entities.prophesy import Prophesy as ProphesyEntity
from source.enumerators.historic import Historic as HistoricEnum

class Analyze:

    def get_all_to_train(self, period: PeriodEnum) -> list[AnalyzeEntity]:
        entities = []
        query = Query()
        query.table('analyzes')
        query.select('analyzes.*')
        query.order('analyzes.created')
        query.where('prophesied.id IS NOT NULL')
        query.where(f'analyzes.period = {Query.quote(period)}')
        query.inner('prophesied', 'prophesied.analyze_id = analyzes.id')
        query.where(f'analyzes.context = {Query.quote(ContextEnum.TRAINING)}')
        models = AnalyzeModel.objects.raw(query.assemble())
        for model in models:
            entities.append(AnalyzeEntity(model))
        return entities
    
    def get_prophesies(self, analyze: AnalyzeEntity, type: HistoricEnum) -> list[ProphesyEntity]:
        query = Query()
        query.table('prophesied')
        query.select('prophesied.*')
        query.order('timelines.datetime')
        query.where(f'prophesied.type = {type.value}')
        query.where(f'prophesied.analyze_id = {analyze.id}')
        query.inner('timelines', 'timelines.id = prophesied.timeline_id')
        models = ProphesyModel.objects.raw(query.assemble())
        list = []
        for model in models:
            list.append(ProphesyEntity(model))
        return list