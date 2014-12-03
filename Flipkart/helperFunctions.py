__author__ = 'serajago'

def user_stopScrolling(w):
    return 'display: block; ' in [e.attribute('style') for e in
                                  w.findElement('div[id="show-more-results"]')] or 'display: block; ' in [
        e.attribute('style') for e in w.findElement('div[id="no-more-results"]')]


def user_stopClicking(w):
    return 'display: block; ' in [e.attribute('style') for e in w.findElement('div[id="no-more-results"]')] or 'display: block; ' in [
        e.attribute('style') for e in w.findElement('div[id="no-more-results"]')]


def user_afterClick(w):
    print("user after click process ")
    w.scrollPageTill(user_stopScrolling, maxTries=100)


