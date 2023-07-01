from dataclasses import dataclass, field
from pathlib import Path
from typing import Collection, List, NamedTuple, Optional

from flask import Flask, render_template, send_file, url_for

app = Flask(__name__)

PAGES = {
    'About': ('about', {}),
    'Projects': ('projects', {
        'SwarmEngine': 'swarm',
        'DOOM: Capture Points System': 'cps',
    })
}


class PortfolioInfo(NamedTuple):
    name: str
    role: str


portfolio_info = PortfolioInfo(
    name="James De Broeck",
    role="Software Development Engineer",
)


@dataclass(frozen=True)
class NavbarSocial(object):
    icon: str
    alt: str
    link: str


def generate_socials() -> Collection[NavbarSocial]:
    return [
        NavbarSocial('email.png', 'Email', 'mailto:debroejm@gmail.com'),
        NavbarSocial('resume.png', 'Resume', url_for('resume')),
        NavbarSocial('linkedin.png', 'LinkedIn', 'https://www.linkedin.com/in/jamesmdebroeck/'),
    ]


class TextBlocks(list, List[str]):
    def __init__(self, *_txt_blocks: str):
        super().__init__([txt.replace('\n', '') for txt in _txt_blocks])


@dataclass(frozen=True)
class PageSection(object):
    title: str
    id: str
    body: TextBlocks


INTRO = TextBlocks(
"""
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin sit amet consequat nisl. Donec fermentum orci ex,
 non lacinia purus vestibulum sit amet. Nunc scelerisque diam eget felis aliquet euismod. Nunc justo lacus, mollis
 et ante non, molestie vehicula eros. Aliquam et nulla odio. Morbi elementum varius ex. Donec egestas, urna a
 malesuada placerat, elit diam vulputate odio, sit amet placerat risus lacus id urna. Phasellus placerat dolor
 pellentesque turpis laoreet maximus. Integer porttitor dui at elit placerat ornare. Quisque vestibulum libero odio,
 quis porttitor ante ullamcorper sed. Nam sollicitudin leo quis nibh dapibus, vitae posuere massa placerat. Donec rutrum
 ante vel neque suscipit, sit amet suscipit lorem pulvinar. Morbi consectetur arcu non mauris venenatis, quis malesuada
 quam rutrum.
"""
)

SECTIONS = [
    PageSection(
        title="Project A",
        id="project-a",
        body=TextBlocks("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin sit amet consequat nisl. Donec fermentum orci ex,
 non lacinia purus vestibulum sit amet. Nunc scelerisque diam eget felis aliquet euismod. Nunc justo lacus, mollis
 et ante non, molestie vehicula eros. Aliquam et nulla odio. Morbi elementum varius ex. Donec egestas, urna a
 malesuada placerat, elit diam vulputate odio, sit amet placerat risus lacus id urna. Phasellus placerat dolor
 pellentesque turpis laoreet maximus. Integer porttitor dui at elit placerat ornare. Quisque vestibulum libero odio,
 quis porttitor ante ullamcorper sed. Nam sollicitudin leo quis nibh dapibus, vitae posuere massa placerat. Donec rutrum
 ante vel neque suscipit, sit amet suscipit lorem pulvinar. Morbi consectetur arcu non mauris venenatis, quis malesuada
 quam rutrum.
""")
    ),
    PageSection(
        title="Project B",
        id="project-b",
        body=TextBlocks("""
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin sit amet consequat nisl. Donec fermentum orci ex,
     non lacinia purus vestibulum sit amet. Nunc scelerisque diam eget felis aliquet euismod. Nunc justo lacus, mollis
     et ante non, molestie vehicula eros. Aliquam et nulla odio. Morbi elementum varius ex. Donec egestas, urna a
     malesuada placerat, elit diam vulputate odio, sit amet placerat risus lacus id urna. Phasellus placerat dolor
     pellentesque turpis laoreet maximus. Integer porttitor dui at elit placerat ornare. Quisque vestibulum libero odio,
     quis porttitor ante ullamcorper sed. Nam sollicitudin leo quis nibh dapibus, vitae posuere massa placerat. Donec rutrum
     ante vel neque suscipit, sit amet suscipit lorem pulvinar. Morbi consectetur arcu non mauris venenatis, quis malesuada
     quam rutrum.
    """)
    ),
]


@app.route('/')
def index():
    return render_template(
        'index.html',
        portfolio_info=portfolio_info,
        nav_pages=PAGES,
        nav_socials=generate_socials(),
        active_page='About',
        intro=INTRO,
        sections=SECTIONS,
    )


@app.route('/resume')
def resume():
    return send_file(Path('files') / 'resume.pdf')


if __name__ == '__main__':
    app.run()
