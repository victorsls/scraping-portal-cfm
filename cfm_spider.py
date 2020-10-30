import scrapy
from decouple import config

from aws_client import DynamoDBClient


class CFMSpider(scrapy.Spider):
    name = 'cfm_spider'
    dynamo_db_client = DynamoDBClient()

    def start_requests(self):
        for url in self.generate_urls():
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response, **kwargs):
        text_element = '::text'
        for result in response.css('div.resultado-mobile-coluna'):
            elements_with_col_12 = result.css('.col-12')
            yield self.dynamo_db_client.create_or_patch_item(table=config('DYNAMO_DB_TABLE'), item={
                'name': result.css('strong::text').extract_first().strip(),
                'crm': result.css('.col-12.col-sm-3::text').extract_first().strip(),
                'registration_date': result.css('.col-12.col-sm-4::text').extract_first().strip(),
                'first_registration_at_state': result.css('.col-12.col-sm-4::text').extract_first().strip(),
                'registration': result.css('.col-12.col-sm-6::text').extract_first().strip(),
                'status': result.css('.col-12.col-sm-6::text')[1].extract().strip(),
                'registration_in_another_state': self.text_to_list(
                    elements_with_col_12[6].css(text_element).extract()[2]
                ),
                'specialties': self.text_to_list(elements_with_col_12[7].css(text_element).extract()[1]),
                'address': elements_with_col_12[8].css(text_element).extract()[2].strip(),
                'phone_numbers': self.text_to_list(elements_with_col_12[9].css(text_element).extract()[2]),
                'image_url': f'https://portal.cfm.org.br{result.css("img::attr(src)").extract_first()}'
            })

    @staticmethod
    def text_to_list(text):
        return [item.strip() for item in text.split(', ') if item]

    @staticmethod
    def generate_urls():
        return [
            f'https://portal.cfm.org.br/index.php?option=com_medicos&especialidadeMedico=55&pagina={page}'
            for page in range(1, config('LAST_PAGE', cast=int) + 1)
        ]
