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
I'm a software engineer with a passion for games. I have experience in cloud computing at AWS, and a specific interest
 in highly-parallelized processing; especially how it can be applied to game systems. I also dabble in rendering here
 and there.
""",
"""
Welcome to my repository of projects.
""",
)

SECTIONS = [
    PageSection(
        title="DOOM: Capture Point Systems",
        id="doom-cps",
        body=TextBlocks(
            "Capture Point Systems is a mod for modern DOOM multiplayer source ports, such as"
            " <a href=\"https://zandronum.com/\">Zandronum</a>. This mod adds a framework for creating \"King of the"
            " Hill\" style capture points. There are a couple gamemodes, most of which use two teams (red vs blue)."
            " Teams either win by capturing all of the points, or by holding a majority of points for the longest time.",
            "<a href=\"https://github.com/MajorSlime/CapturePointSystems\">Core Framework</a>",
            "<a href=\"https://github.com/MajorSlime/CapturePointSystemsMapPackDoom\">DOOM Map Pack</a>",
        )),
    PageSection(
        title="SwarmEngine",
        id="swarm-engine",
        body=TextBlocks("""
""")),
    PageSection(
        title="SimpleBlend",
        id="simple-blend",
        body=TextBlocks("""
""")),
    PageSection(
        title="Reversi",
        id="reversi",
        body=TextBlocks("""
""")),
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
