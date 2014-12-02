__doc__ = 'Interface to qt webkit for parsing JavaScript dependent webpages'

import sys
import os
import re
# import urllib2
import urllib.request
import random
from time import time, sleep
from datetime import datetime

# for using native Python strings
import sip

sip.setapi('QString', 2)
from PyQt4.QtGui import *
from PyQt4.Qt import *
from PyQt4.QtCore import *
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtWebKit import *
from PyQt4.QtNetwork import QNetworkAccessManager, QNetworkProxy, QNetworkRequest, QNetworkReply, QNetworkDiskCache

"""
# XXX some seg faults with subclassing QNetworkAccessManager
from PySide.QtGui import QApplication, QDesktopServices, QImage, QPainter
from PySide.QtCore import QByteArray, QUrl, QTimer, QEventLoop, QIODevice, QObject
from PySide.QtWebKit import QWebFrame, QWebView, QWebPage, QWebSettings
from PySide.QtNetwork import QNetworkAccessManager, QNetworkProxy, QNetworkRequest, QNetworkReply, QNetworkDiskCache
"""

import scrapperUtils
import scrapperConstants as const


class ScrapperNetworkAccessManager(QNetworkAccessManager):
    """Subclass QNetworkAccessManager for logging error messages
    """

    def __init__(self):
        QNetworkAccessManager.__init__(self)
        self.reqCount = 0


    def createRequest(self, op, request, device):
        # prefer valid cache instead of network
        self.reqCount = self.reqCount + 1
        if re.match(".*?pubads\.g\.doubleclick\.net*", request.url().toString()):
            request.setUrl(QUrl("http://img6a.flixcart.com/www/prod/images/flipkart_india-e5f5aa9f.png"))
            # print "REQ :",self.reqCount," ",request.url()

        request.setAttribute(QNetworkRequest.CacheLoadControlAttribute, QNetworkRequest.PreferCache)

        reply = QNetworkAccessManager.createRequest(self, op, request, device)
        reply.error.connect(self.logNetworkErrors)

        return reply


    def logNetworkErrors(self, error):
        errors = {
            0: "QNetworkReply.NoError",
            1: "QNetworkReply.ConnectionRefusedError",
            2: "QNetworkReply.RemoteHostClosedError",
            3: "QNetworkReply.HostNotFoundError",
            4: "QNetworkReply.TimeoutError",
            5: "QNetworkReply.OperationCanceledError",
            6: "QNetworkReply.SslHandshakeFailedError",
            7: "QNetworkReply.TemporaryNetworkFailureError",
            101: "QNetworkReply.ProxyConnectionRefusedError",
            102: "QNetworkReply.ProxyConnectionClosedError",
            103: "QNetworkReply.ProxyNotFoundError",
            104: "QNetworkReply.ProxyTimeoutError",
            105: "QNetworkReply.ProxyAuthenticationRequiredError",
            201: "QNetworkReply.ContentAccessDenied",
            202: "QNetworkReply.ContentOperationNotPermittedError",
            203: "QNetworkReply.ContentNotFoundError",
            204: "QNetworkReply.AuthenticationRequiredError",
            205: "QNetworkReply.ContentReSendError",
            301: "QNetworkReply.ProtocolUnknownError",
            302: "QNetworkReply.ProtocolInvalidOperationError",
            99: "QNetworkReply.UnknownNetworkError",
            199: "QNetworkReply.UnknownProxyError",
            299: "QNetworkReply.UnknownContentError",
            399: "QNetworkReply.ProtocolFailure"
        }
        scrapperUtils.scrapperLog(const.LogCritical,
                                  ("NWError %d: %s %s") % (error, errors[error], self.sender().url().toString()))


class WebPage(QWebPage):
    def __init__(self, user_agent=None, confirm=True):
        QWebPage.__init__(self)

    def userAgentForUrl(self, url):
        return None

    def javaScriptAlert(self, frame, message):
        pass

    def javaScriptConfirm(self, frame, message):
        return True

    def javaScriptPrompt(self, frame, message, default):
        pass

    def javaScriptConsoleMessage(self, message, line_number, source_id):
        pass

    def shouldInterruptJavaScript(self):
        return True


class Browser(QWebView):
    """
    TODO:
        - we need error handling - a must have
        - cap/timeout on clickwaits and scrollwaits
    """

    def __init__(self, gui=False, loadImages=False, timeout=20):
        self.app = QApplication(sys.argv)  # must instantiate first

        webView = QWebView.__init__(self)

        manager = ScrapperNetworkAccessManager()

        # create a new webpage using default user agents
        webpage = WebPage()
        # use our network access manager
        webpage.setNetworkAccessManager(manager)

        self.setPage(webpage)
        self.setHtml('<html><head></head><body>No content loaded</body></html>', QUrl('http://localhost'))
        self.timeout = timeout
        self.jquery_lib = None

        self.settings().setAttribute(QWebSettings.PluginsEnabled, False)
        self.settings().setAttribute(QWebSettings.JavaEnabled, False)
        self.settings().setAttribute(QWebSettings.AutoLoadImages, loadImages)
        self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)

        self.urlChanged.connect(self.eventUrlChanged)
        self.defaultProxy = None
        # self.page().saveFrameStateRequested.connect(self.eventUrlChanged)
        if gui: self.show()


    def __del__(self):
        # not sure why, but to avoid seg fault need to release the QWebPage manually
        self.setPage(None)

    # we would like to keep one browser object and reload new
    # pages with different proxy and cache config
    # while processing new pages
    def setDefaultProxy(self, host, port=None, username=None, password=None):
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.HttpProxy)
        if username:
            proxy.setUser(username)
        if password:
            proxy.setPassword(password)
        if port:
            proxy.setPort(port)

        proxy.setHostName(host)
        self.defaultProxy = proxy
        self.page().networkAccessManager().setProxy(proxy)

    def restoreDefaultProxy(self):
        if not self.defaultProxy:
            return
        self.page().networkAccessManger().setProxy(self.defaultProxy)

    def setTempProxy(self, host, port=None, username=None, password=None):
        proxy = QNetworkProxy()
        proxy.setType(QNetworkProxy.HttpProxy)
        if username:
            proxy.setUser(username)
        if password:
            proxy.setPassword(password)
        if port:
            proxy.setPort(port)
        proxy.setHostName(host)
        self.page().networkAccessManager().setProxy(proxy)


    def setCache(self, cacheDir, cacheSize):
        cache = QNetworkDiskCache()
        cache.setCacheDirectory(cacheDir)
        cache.setMaximumCacheSize(cacheSize * 1024 * 1024)
        self.page().networkAccessManager().setCache(cache)

    def currentUrl(self):
        return str(self.url().toString())

    def currentHtml(self):
        return (unicode(self.page().mainFrame().toHtml())).encode('utf-8')

    def decodedUrl(self, url=None):
        if url is None:
            url = self.url()
        return QUrl.fromEncoded(url)


    def loadPage(self, url, numRetries=1):
        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)

        # register slots
        timer.timeout.connect(loop.quit)
        self.loadFinished.connect(loop.quit)

        # load url
        self.load(QUrl(url))

        # start the timer and event loop and wait for the load to complete
        timer.start(self.timeout * 1000)
        loop.exec_()

        if timer.isActive():
            # downloaded successfully
            timer.stop()
            return True
        else:
            # did not download in time
            if numRetries > 0:
                scrapperUtils.scrapperLog(const.LogError, ("Timeout for url %s \n") % (url))
                return self.loadPage(url, numRetries - 1)
            else:
                scrapperUtils.scrapperLog(const.LogError, ("RetryLimit for url %s \n") % (url))
                return False


    def waitSecs(self, secs=1):
        # wait for some time before checking
        loop = QEventLoop()
        timer = QTimer()
        timer.setSingleShot(True)
        # register slots
        timer.timeout.connect(loop.quit)
        # start the timer and give .5 secs for the page to load
        # dynamic contents
        self.app.processEvents()
        timer.start(secs * 1000)
        loop.exec_()
        timer.stop()


    def evaluateJavaScript(self, script):
        self.app.processEvents()
        return self.page().mainFrame().evaluateJavaScript(script).toString()

    def injectJquery(self):
        if self.jqueryLib is None:
            url = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js'
            self.jqueryLib = urllib.request.urlopen(url).read()
        self.js(self.jquery_lib)


    # wait for some condition, this waits
    # till the stopWaiting functions says
    # to stop
    # True - if the waited-for event has occurred
    # False - if max tries have reached
    def waitTill(self, stopWaiting, maxTries=20, timerStep=500):
        # convert to # of loops
        while not stopWaiting(self) and maxTries:
            maxTries = maxTries - 1
            # wait for some time before checking
            loop = QEventLoop()
            timer = QTimer()
            timer.setSingleShot(True)
            # register slots
            timer.timeout.connect(loop.quit)
            # start the timer and give .5 secs for the page to load
            # dynamic contents
            timer.start(timerStep)
            loop.exec_()
        timer.stop()
        if not maxTries:
            # log error
            scrapperUtils.scrapperLog(const.LogError, "Timeout")
            return False
        else:
            return True

    def clickElement(self, pattern, afterClick=None):
        self.app.processEvents()
        for e in self.findElement(pattern):
            e.evaluateJavaScript("var evObj = document.createEvent('MouseEvents');\
			 evObj.initEvent('click', true, true); this.dispatchEvent(evObj);")
        # do what ever you want after this click
        # like wait for an element to load,
        # scroll page, fill some element anything.
        if afterClick:
            afterClick(self)

    def clickElementTill(self, pattern, stopClicking, maxTries=20, afterClick=None, timerStep=500):
        while not stopClicking(self) and maxTries:
            maxTries = maxTries - 1
            self.clickElement(pattern, afterClick=afterClick)
            # wait for some time before checking
            loop = QEventLoop()
            timer = QTimer()
            timer.setSingleShot(True)
            # register slots
            timer.timeout.connect(loop.quit)
            # start the timer and give .5 secs for the page to load
            # dynamic contents
            timer.start(timerStep)
            loop.exec_()
            timer.stop()
        if not maxTries:
            # lof error
            scrapperUtils.scrapperLog(const.LogError, "Timeout")
            return False
        else:
            # we reached end of clicking successfuly
            return True


    def scrollPage(self, degrees=180, afterScroll=None):
        # do 180 degree scroll down
        event = QWheelEvent(QCursor.pos(), -1 * (degrees / 15) * 120, Qt.MouseButtons(), Qt.KeyboardModifiers(),
                            Qt.Vertical)
        QCoreApplication.postEvent(self, event)
        if afterScroll:
            afterScroll(self)

    def scrollPageTill(self, stopScrolling, maxTries=20, afterScroll=None, timerStep=500):
        while not stopScrolling(self) and maxTries:
            maxTries = maxTries - 1
            self.scrollPage(afterScroll=afterScroll)
            # wait for some time before checking
            loop = QEventLoop()
            timer = QTimer()
            timer.setSingleShot(True)
            # register slots
            timer.timeout.connect(loop.quit)
            # start the timer and give .5 secs for the page to load
            # dynamic contents
            timer.start(timerStep)
            loop.exec_()
        timer.stop()
        if not maxTries:
            # log error
            scrapperUtils.scrapperLog(const.LogError, "Timeout")
            return False
        else:
            return True


    def setElementAttr(self, pattern, name, value):
        elements = self.findElement(pattern)
        if len(elements) == 0:
            scrapperUtils.scrapperLog(const.LogError, ("ElemNotFound %s") % (pattern))
        for e in elements:
            e.setAttribute(name, value)

    def getElementAttr(self, pattern, name):
        return str(self.page().mainFrame().findFirstElement(pattern).attribute(name))

    def fillElement(self, pattern, value):
        elements = self.findElement(pattern)
        if len(elements) == 0:
            scrapperUtils.scrapperLog(const.LogError, ("ElemNotFound %s") % (pattern))
        for e in elements:
            tag = str(e.tagName()).lower()
            if tag == 'input':
                e.evaluateJavaScript('this.value = "%s"' % value)
            else:
                e.setPlainText(value)

    def findElement(self, pattern):
        return self.page().mainFrame().findAllElements(pattern).toList()


    def readCacheData(self, url):
        record = self.page().networkAccessManager().cache().data(QUrl(url))
        if record:
            data = record.readAll()
            record.reset()
        else:
            data = None
        return data

    def screenShot(self, output_file):
        frame = self.page().mainFrame()
        self.page().setViewportSize(frame.contentsSize())
        image = QImage(self.page().viewportSize(), QImage.Format_ARGB32)
        painter = QPainter(image)
        frame.render(painter)
        painter.end()
        image.save(output_file)

    def closeEvent(self, event):
        sys.exit(0)

    def url_changed(self, url):
        print(url)
    def eventUrlChanged(self, url):
        pass
