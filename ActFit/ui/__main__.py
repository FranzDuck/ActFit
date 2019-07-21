import sys
from .app import App


def main():
    sys.exit(
        App.run(
            src="""def f(xs, m, b, c):
    return m * np.sin(b * xs) + c

def g(xs, a, b, c, d, e):
    return a * np.power(xs - e, 3) + b * np.power(xs - e, 2) + c * (xs - e) + d

xs = np.linspace(0, np.pi*2, 100)

data = np.sin(xs) + np.random.rand(100)*3"""
        )
        or 0
    )


if __name__ == "__main__":
    main()
