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
    gallery: Collection[str] = field(default_factory=list)


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
            " Hill\" style capture points, in a style that closely resembles Team Fortress 2's Control Points. There"
            " are a couple game modes, most of which use two teams (red vs blue). Teams either win by capturing all of"
            " the points, or by holding a majority of points for the longest time.",
            "The game mode is achieved by using Zandronum's base \"Team Game\" game mode, which allows for scripting"
            " custom rules to control points and win conditions. Scripts are written in"
            " <a href=\"https://zdoom.org/wiki/ACS\">Action Code Script (ACS)</a>, which is Doom's own custom scripting"
            " language.",
            "The game mode scripting is <a href=\"https://zdoom.org/wiki/IWAD\">IWAD</a> agnostic, meaning maps can be"
            " made for Doom, Chex Quest, or any other game that runs using Zandronum or similar source-ports. A"
            " first-party set of maps for both Chex Quest and Doom are provided.",
            "<span class=\"center\"><a href=\"https://github.com/MajorSlime/CapturePointSystems\">Core Framework</a>"
            " • <a href=\"https://github.com/MajorSlime/CapturePointSystemsMapPackDoom\">DOOM Map Pack</a></span>",
        ),
        gallery=[
            'CQ_CPS02.png',
            'CQ_CPS03.png',
            'CQ_CPS05.png',
        ],
    ),
    PageSection(
        title="SwarmEngine",
        id="swarm-engine",
        body=TextBlocks(
            "Video game development still seems to be catching up with utilizing parallel computing more often, so"
            " SwarmEngine is a project created to experiment with a highly parallelized game engine. It started as a"
            " college capstone project, but has been kept around as a workspace to test out new ideas.",
            "The overall design of the engine is to separate different aspects and responsibilities into different"
            " worker threads; rendering in one, physics in others, etc. At the original time of creation, OpenGL was"
            " used, so there is only one render thread as"
            " <a href=\"https://www.gamingonlinux.com/2017/02/opengl-multi-threading-what-it-is-and-what-it-means/\">"
            "OpenGL contexts don't like being shared across threads</a>. At some point, the idea is to go back and"
            " switch to Vulkan, as that deals with parallel threads much better.",
            "Physics and other calculations take place in separate worker threads. There have been several experiments"
            " with how to sync this data with the render threads. The simplest is just to sync and copy data around at"
            " regular intervals, with the relevant threads utilizing barriers and sending the data needed for rendering"
            " over to the render thread/s. My favorite version though, is to have the data threads expose a read-only"
            " version of their internal data that is updated on each thread's own time, and can be read by the render"
            " thread/s at a separate cadence that is more tied to framerate. This of course has implications with data"
            " being modified at different rates than it is rendered, but can result in significantly less slowdown due"
            " to synchronizing.",
            "Currently, the project is in C++, but there is some interest in re-writing it in Rust as an effort to see"
            " how well Rust could be used for an engine like this, given Rust's inclination towards parallelism.",
            "<span class=\"center\"><a href=\"https://github.com/debroejm/SwarmEngine\">SwarmEngine</a></span>",
        )),
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
