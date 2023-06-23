from pathlib import Path
from typing import Collection, NamedTuple

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


class NavbarSocial(NamedTuple):
    icon: str
    alt: str
    link: str


def generate_socials() -> Collection[NavbarSocial]:
    return [
        NavbarSocial('email.png', 'Email', 'mailto:debroejm@gmail.com'),
        NavbarSocial('resume.png', 'Resume', url_for('resume')),
        NavbarSocial('linkedin.png', 'LinkedIn', 'https://www.linkedin.com/in/jamesmdebroeck/'),
    ]


@app.route('/')
def index():
    return render_template(
        'index.html',
        portfolio_info=portfolio_info,
        nav_pages=PAGES,
        nav_socials=generate_socials(),
        active_page='About',
    )


@app.route('/resume')
def resume():
    return send_file(Path('files') / 'resume.pdf')


if __name__ == '__main__':
    app.run()
