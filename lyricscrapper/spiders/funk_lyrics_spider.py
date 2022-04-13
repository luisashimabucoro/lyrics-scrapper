import scrapy as sp


class FunkSpider(sp.Spider):
    name = 'funk-lyrics'
    start_urls = ['https://www.letras.mus.br/mais-acessadas/funk/']

    def parse(self, response):
        url = 'https://m.letras.mus.br'

        artists_links = response.css('ol.top-list_art li a::attr(href)')

        for link in artists_links:
            link = url + link.get()
            yield response.follow(link, callback=self.parse_artist)

    def parse_artist(self, response):
        url = 'https://m.letras.mus.br'
        song_links = response.css('ul.artist-songlist li.artist-songlist-item a::attr(href)')
        for link in song_links:
            link = url + link.get()
            yield response.follow(link, callback=self.parse_song)
    
    def parse_song(self, response):
        song_title = response.css('div.lyric-title h1::text')
        artist = response.css('div.lyric-title h2 a::text')
        song_paragraphs = response.css('div.lyric-cnt p::text')

        lyrics = ''
        for text in song_paragraphs:
            lyrics += text.get().lower() + '\\n'

        if len(lyrics):
            yield {
                'artist' : artist.get(),
                'song_title' : song_title.get(),
                'lyrics' : lyrics
            }