class AudioContextMock {
    constructor() {
    }
}

class webkitAudioContextMock {
    constructor() {
    }
}

var indexedDB = {}
var localStorage = {
    "b1b1": "1",
    "XHS_STRATEGY_BOX": "{\"firstVisit-\":false}",
    "HOME_FEED_CURSOR_SCORE": "1.6846402299610028E9",
    "p1": "8",
    "saluteby": "lx",
    getItem: function getItem(x) {
        return null
    },
    removeItem: function removeItem(x) {
    },
};
var navigator = {
    plugins: {},
    webdriver: false,
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    languages: ["zh-CN", "zh"],
    appCodeName: "Mozilla",
    appName: "Netscape",
    appVersion: "5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    platform: "Win32"
};
var location = {
    toString: function () {
        return location.href
    },
    "protocol": "https:",
    "ancestorOrigins": {},
    // "href": "https://www.xiaohongshu.com/user/profile/63170c89000000000f006ee6",
    // "origin": "https://www.xiaohongshu.com",
    // "host": "www.xiaohongshu.com",
    // "hostname": "www.xiaohongshu.com",
    "port": "",
    // "pathname": "/user/profile/63170c89000000000f006ee6",
    "search": "",
    "hash": "",

};
var document = {
    createEvent: function createEvent() {
    },
    location: location,
    cookie: '',
    vlinkColor: "",
    referrer: 'https://www.xiaohongshu.com',
    fgColor: "",
    dir: "",
    addEventListener: function addEventListener(x) {
    },
    createElement: function createElement(x) {
        return canvas
    }
};
var canvas = {
    toDataURL: function toDataURL() {
    },
    getContext: function getContext(x) {
    }
};

var window = {
    navigator: navigator,
    location: location,
    document: document,
    indexedDB: indexedDB,
    localStorage: localStorage,
    RegExp: RegExp,
    screen: {
        "availHeight": 1040,
        "availLeft": 0,
        "availTop": 0,
        "availWidth": 1920,
        "colorDepth": 24,
        "height": 1080,
        "isExtended": false,
        "onchange": null,
        "pixelDepth": 24,
        "width": 1920,
        "orientation": {angle: 0, type: 'landscape-primary', onchange: null, 'salute': 'lx'}
    },
    setInterval: setInterval,
    isNaN: isNaN,
    isFinite: isFinite,
    eval: eval,
    unescape: unescape,
    encodeURIComponent: encodeURIComponent,
    encodeURI: encodeURI,
    decodeURIComponent: decodeURIComponent,
    decodeURI: decodeURI,
    Map: Map,
    Math: Math,
    JSON: JSON,
    Date: Date,
    String: String,
    parseInt: parseInt,
    parseFloat: parseFloat,
    Array: Array,
    Number: Number,
    Function: Function,
    Object: Object,
    devicePixelRatio: 1,
    AudioContext: AudioContextMock,
    webkitAudioContext: {},
    webkitAudioContextMock: webkitAudioContextMock,
    openDatabase: function () {
    },
    sdt_source_init: true,
};

const crypto = require('crypto');
let key = 'fn7cxhamzqet4ltw'
let iv = '3w5zacaub8dqv9zq'
key = Buffer.from(key);
iv = Buffer.from(iv);



var encrypt = function (data) {
    const cipher = crypto.createCipheriv('aes-128-cbc', key, iv);
    let encrypted = cipher.update(data, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    return encrypted;
};
function decrypt(encryptedText) {
    const decipher = crypto.createDecipheriv('aes-128-cbc', key, iv);
    let decrypted = decipher.update(encryptedText, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    return decrypted;
}
var esm_typeof = {
    Z: function (t) {
        return typeof t;
    },
};
var r = [
    "xUKNL",
    "jUrZI",
    "rviFu",
    "join",
    "get",
    "LjDtD",
    "ZJHyP",
    "wOmGY",
    "enumera",
    "aONWR",
    "string",
    "kQpMi",
    "mZPJZ",
    "Ysiay",
    "czxKn",
    "|5|6|4|",
    "prototy",
    "jklmnop",
    "MuYbw",
    "diDwk",
    "TRFtx",
    "drDHI",
    "WLARA",
    "xyz0123",
    "asBytes",
    "|6|0|1|",
    "JOtEi",
    "Oialn",
    "OQrEi",
    "uPnXq",
    "VWXYZab",
    "cIbFa",
    "qYuta",
    "QDOZZ",
    "MahgM",
    "iRXZq",
    "22098XlFGYn",
    "mmLKn",
    "jMcIE",
    "stringi",
    "[object",
    "nYqUQ",
    "jSgjk",
    "ucyEo",
    "iewJI",
    "vgTwl",
    "DnNGR",
    "oBytes",
    "Xtwzk",
    "aqlTy",
    "JWnPK",
    "1|0|2|4",
    "qrstuvw",
    "_gg",
    "QLthP",
    "FJIWy",
    "yRnhISG",
    "pjUsr",
    "KAwuh",
    "Thhoa",
    "jarkJ",
    "WjRNN",
    "asStrin",
    "x3VT16I",
    "357835LaQWjW",
    "SkIJl",
    "size",
    "iyorr",
    "iHUeL",
    "tTanW",
    "tNusJ",
    "NiSrP",
    "eAt",
    "TCArD",
    "a2r1ZQo",
    "iamspam",
    "bOnfu",
    "UNSKg",
    "HIJKLMN",
    "ZfMKC",
    "bJhXU",
    "zwAAc",
    "JYxWY",
    "lUAFM97",
    "mwaRe",
    "EzYWD",
    "replace",
    "uOtUJ",
    "__esMod",
    "ViQWI",
    "aCMFL",
    "EAKSd",
    "ule",
    "pqnFP",
    "qYDsL",
    "270726pnaYfG",
    "glBZG",
    "OwjMq",
    "YGrjc",
    "ZhAcd",
    "JDqFL",
    "456789+",
    "kEjQs",
    "lWhbD",
    "OaLTI",
    "dXlgm",
    "cVte9UJ",
    "ctor",
    "hwomB",
    "wDtJz",
    "constru",
    "ABHuC",
    "zDETq",
    "SYNeA",
    "BGbij",
    "ionFq",
    "QzaNS",
    "7|3|5|4",
    "YlZGp",
    "Bjniw",
    "ZITuN",
    "KPTzH",
    "HrBeq",
    "xobsT",
    "kXJkC",
    "QSrEZ",
    "ENXtO",
    "FYbRJ",
    "wOcza/L",
    "_hh",
    "dVXMb",
    "ppkua",
    "WgamZ",
    "HuwCW",
    "362424fnLCuh",
    "charCod",
    "HhPqg",
    "ODunI",
    "eJzqq",
    "charAt",
    "JGAgI",
    "ZmserbB",
    "TURcG",
    "WyrqF",
    "iYJzH",
    "VIwfH",
    "tzzOB",
    "YgiCH",
    "byyMQ",
    "ELxEv",
    "0DSfdik",
    "HRihr",
    "_ii",
    "aDsrp",
    "ble",
    "jTGtW",
    "configu",
    "cXiYW",
    "56kSpAsC",
    "158KIldlA",
    "oHQtNP+",
    "BHavO",
    "PCIlh",
    "QatIf",
    "IKyqh",
    "Words",
    "Qwnrg",
    "44lQAgNu",
    "cdefghi",
    "nTwxD",
    "RHteb",
    "coqPr",
    "rJwmI",
    "aBoeK",
    "default",
    "exports",
    "rceYY",
    "isArray",
    "mdKKO",
    "kzxWE",
    "DeBtm",
    "tjjUn",
    "vJEcD",
    "LpfE8xz",
    "bin",
    "HKazo",
    "rable",
    "call",
    "wordsTo",
    "zBiyt",
    "GrsGL",
    "fqulF",
    "jevwl",
    "mxfLj",
    "xlUnt",
    "q42KWYj",
    "endian",
    "eEqDc",
    "oyGAZ",
    "bytesTo",
    "OzjuJ",
    "IfwWq",
    "ize",
    "6648810piiNEz",
    "lTHdy",
    "vDLZJ",
    "stringT",
    "A4NjFqY",
    "GkjTz",
    "eooJA",
    "substr",
    "veNiI",
    "LYfDp",
    "ljKsP",
    "jJYWG",
    "bcYAf",
    "srikB",
    "utf8",
    "qTbeY",
    "yqRzd",
    "|3|5",
    "bjbAy",
    " Array]",
    "rMbXP",
    "u5wPHsO",
    "test",
    "gMIMC",
    "Deyqv",
    " argume",
    "ABCDEFG",
    "undefin",
    "split",
    "QTlsj",
    "_isBuff",
    "OPQRSTU",
    "Illegal",
    "loSen",
    "navigat",
    "ObwNo",
    "qPbcq",
    "7182692QogvXX",
    "tvqSn",
    "DGptJ",
    "HhTfW",
    "avIYx",
    "defineP",
    "PFQbW",
    "CjFyM",
    "toStrin",
    "yMWXS",
    "yMyOy",
    "0XTdDgM",
    "eXkru",
    "_blocks",
    "indexOf",
    "mbBQr",
    "lBuRH",
    "HzGjH",
    "HNErV",
    "mEokX",
    "userAge",
    "UpmtD",
    "sgomx",
    "KDfKS",
    "OTbSq",
    "lxMGW",
    "0|3|2|1",
    "dfWyB",
    "lWzAd",
    "eyXTL",
    "5624qreyZK",
    "pow",
    "IJstz",
    "LMlMB",
    "INlwI",
    "lRulU",
    "TCgZh",
    "_digest",
    "UBhIl",
    "fLtZZ",
    "FYSKq",
    "2|8|0",
    "IoCeZ",
    " Object",
    "UuTvI",
    "lNKLD",
    "String",
    "Bytes",
    "rBVvW",
    "KblCWi+",
    "pRaIH",
    "roperty",
    "vTINI",
    "atLE",
    "functio",
    "Udqoy",
    "nt ",
    "htSWx",
    "hEwRK",
    "encodin",
    "sCSVK",
    "VuAZF",
    "xeIIy",
    "RBjMb",
    "taTrq",
    "vDLFJ",
    "bPkya",
    "HzimH",
    "nCffO",
    "BWbtU",
    "2|8",
    "slice",
    "lxMGQ",
    "tTiwe",
    "JDhJB",
    "rCode",
    "gNDzY",
    "wJkyu",
    "cCZFe",
    "RNGSl",
    "floor",
    "clYIu",
    "vLiwz",
    "BiNSE",
    "MtYWB",
    "fromCha",
    "StNOc",
    "|7|5|3|",
    "9|1|4|6",
    "length",
    "UNYAE",
    "pngG8yJ",
    "hasOwnP",
    "pYeWu",
    "wTjkk",
    "Bvk6/7=",
    "KTmgk",
    "bIGxm",
    "readFlo",
    "LFZch",
    "_ff",
    "1|3|4|2",
    "binary",
    "LLdJZ",
    "ZofOU",
    "6399uFPxTQ",
    "push",
    "YntPT",
    "kSGXO",
    "random",
    "HfpCU",
    "hECvuRX",
    "getTime",
    "iwSyV",
    "alert",
    "LKMcb",
    "DJVdg",
    "Hex",
    "URzKO",
    "CxjtF",
    "ZVOCs",
    "isBuffe",
    "vGpbT",
    "rotl",
    "udFrB",
    "CnbsH",
    "crLST",
];
function a0_0x10f4ac(t, e) {
    return a0_0x3693(e - -570, t);
}
var a0_0x3693 = function (t, e) {
    return r[(t -= 131)];
};
for (
    var encrypt_lookup = [],
        encrypt_code =
            a0_0x10f4ac(-179, -298) +
            a0_0x10f4ac(-369, -279) +
            a0_0x10f4ac(-467, -311) +
            a0_0x10f4ac(-267, -108) +
            a0_0x10f4ac(-328, -244) +
            a0_0x10f4ac(-293, -289) +
            a0_0x10f4ac(-251, -376) +
            a0_0x10f4ac(-448, -356) +
            a0_0x10f4ac(-241, -88) +
            "5",
        encrypt_i = 0,
        encrypt_len = encrypt_code[a0_0x10f4ac(16, -110)];
    encrypt_i < encrypt_len;
    ++encrypt_i
)
    encrypt_lookup[encrypt_i] = encrypt_code[encrypt_i];
function encrypt_encodeChunk(t, e, r) {
    var n,
        o = 165,
        i = 246,
        a = 205,
        u = 353,
        s = 162,
        c = 17,
        l = 351,
        f = 191,
        p = 139,
        h = 79,
        d = 86,
        v = 233,
        g = 270,
        m = 166,
        y = {
            hwomB: function (t, e) {
                return t < e;
            },
            iHUeL: function (t, e) {
                return t & e;
            },
            ELxEv: function (t, e) {
                return t << e;
            },
            lBuRH: function (t, e) {
                return t << e;
            },
            SkIJl: function (t, e) {
                return t & e;
            },
            JYxWY: function (t, e) {
                return t + e;
            },
            CxjtF: function (t, e) {
                return t(e);
            },
        },
        w = [];
    function _(t, e) {
        return a0_0x10f4ac(t, e - m);
    }
    for (var b = e; y[_(-63, -o)](b, r); b += 3)
        (n =
            y[_(-i, -a)](y[_(-166, -124)](t[b], 16), 16711680) +
            y[_(-u, -205)](y[_(s, -c)](t[b + 1], 8), 65280) +
            y[_(-l, -208)](t[y[_(-350, -f)](b, 2)], 255)),
            w[_(p, 73)](y[_(h, d)](encrypt_tripletToBase64, n));
    return w[_(-v, -g)]("");
}
function encrypt_tripletToBase64(t) {
    var e = 11,
        r = 15,
        n = 199,
        o = 34,
        i = 4,
        a = 102,
        u = 276,
        s = 205,
        c = 218,
        l = 11,
        f = 115,
        p = 34,
        h = 161,
        d = 123,
        v = 335,
        g = {};
    function m(t, e) {
        return a0_0x10f4ac(e, t - v);
    }
    (g[m(205, 328)] = function (t, e) {
        return t + e;
    }),
        (g[m(e, 53)] = function (t, e) {
            return t >> e;
        }),
        (g[m(r, n)] = function (t, e) {
            return t & e;
        }),
        (g[m(o, i)] = function (t, e) {
            return t >> e;
        }),
        (g[m(-a, -u)] = function (t, e) {
            return t & e;
        });
    var y = g;
    return (
        y[m(s, c)](
            encrypt_lookup[63 & y[m(l, -75)](t, 18)],
            encrypt_lookup[y[m(r, f)](y[m(p, h)](t, 12), 63)]
        ) +
        encrypt_lookup[(t >> 6) & 63] +
        encrypt_lookup[y[m(-a, -d)](t, 63)]
    );
}
function encrypt_encodeUtf8(t) {
    var e = 185,
        r = 410,
        n = 480,
        o = 222,
        i = 194,
        a = 165,
        u = 147,
        s = 290,
        c = 460,
        l = 472,
        f = 497,
        p = 462,
        h = 286,
        d = 209,
        v = 223,
        g = 590,
        m = {
            bIGxm: function (t, e) {
                return t(e);
            },
            MahgM: function (t, e) {
                return t < e;
            },
            czxKn: function (t, e) {
                return t === e;
            },
            clYIu: function (t, e) {
                return t + e;
            },
        },
        y = m["bIGxm"](encodeURIComponent, t),
        w = [];
    function _(t, e) {
        return a0_0x10f4ac(t, e - g);
    }
    for (var b = 0; m["MahgM"](b, y["length"]); b++) {
        var E = y["charAt"](b);
        if (m["czxKn"](E, "%")) {
            var T =
                    y["charAt"](m["clYIu"](b, 1)) +
                    y["charAt"](m["clYIu"](b, 2)),
                x = parseInt(T, 16);
            w["push"](x), (b += 2);
        } else w["push"](E["charCodeAt"](0));
    }
    return w;
}
function encrypt_b64Encode(t) {
    var e = 664,
        r = 634,
        n = 448,
        o = 599,
        i = 315,
        a = 416,
        u = 512,
        s = 361,
        c = 406,
        l = 487,
        f = 496,
        p = 333,
        h = 630,
        d = 639,
        v = 548,
        g = 582,
        m = 447,
        y = 468,
        w = 375,
        _ = 331,
        b = 149,
        E = 382,
        T = 265,
        x = 625,
        k = 570,
        S = 551,
        L = 582,
        O = 581,
        R = 638,
        I = 618,
        A = 606,
        C = 429,
        N = 651,
        P = 667,
        B = 817,
        F = 333,
        j = 567,
        M = 747,
        D = 561,
        q = 570,
        U = 676,
        Z = 840,
        G = 240,
        H = {
            udFrB: function (t, e) {
                return t % e;
            },
            cCZFe: function (t, e) {
                return t === e;
            },
            jevwl: function (t, e) {
                return t - e;
            },
            aqlTy: function (t, e) {
                return t + e;
            },
            rceYY: function (t, e) {
                return t >> e;
            },
            OwjMq: function (t, e) {
                return t & e;
            },
            kSGXO: function (t, e) {
                return t << e;
            },
            veNiI: function (t, e) {
                return t === e;
            },
            QLthP: function (t, e) {
                return t + e;
            },
            wDtJz: function (t, e) {
                return t + e;
            },
            nYqUQ: function (t, e) {
                return t & e;
            },
            TCArD: function (t, e) {
                return t << e;
            },
            RHteb: function (t, e) {
                return t - e;
            },
            mZPJZ: function (t, e) {
                return t < e;
            },
            zDETq: function (t, e, r, n) {
                return t(e, r, n);
            },
            YlZGp: function (t, e) {
                return t > e;
            },
        };
    function V(t, e) {
        return a0_0x10f4ac(e, t - -G);
    }
    for (var Y = "0|3|2|1|5|6|4|7"["split"]("|"), W = 0; ; ) {
        switch (Y[W++]) {
            case "0":
                var z;
                continue;
            case "1":
                var X = [];
                continue;
            case "2":
                var K = H["udFrB"](J, 3);
                continue;
            case "3":
                var J = t["length"];
                continue;
            case "4":
                H["cCZFe"](K, 1)
                    ? ((z = t[H["jevwl"](J, 1)]),
                      X["push"](
                          H["aqlTy"](
                              encrypt_lookup[H["rceYY"](z, 2)] +
                                  encrypt_lookup[
                                      H["OwjMq"](H["kSGXO"](z, 4), 63)
                                  ],
                              "=="
                          )
                      ))
                    : H["veNiI"](K, 2) &&
                      ((z = H["kSGXO"](t[J - 2], 8) + t[H["jevwl"](J, 1)]),
                      X[V(-333, -T)](
                          H[V(-x, -505)](
                              H[V(-k, -S)](
                                  encrypt_lookup[z >> 10],
                                  encrypt_lookup[H[V(-L, -O)](z >> 4, 63)]
                              ) +
                                  encrypt_lookup[
                                      H[V(-R, -I)](H[V(-A, -C)](z, 2), 63)
                                  ],
                              "="
                          )
                      ));
                continue;
            case "5":
                var $ = 16383;
                continue;
            case "6":
                for (
                    var Q = 0, tt = H[V(-509, -N)](J, K);
                    H[V(-P, -B)](Q, tt);
                    Q += $
                )
                    X[V(-F, -153)](
                        H[V(-j, -M)](
                            encrypt_encodeChunk,
                            t,
                            Q,
                            H[V(-D, -413)](Q + $, tt)
                                ? tt
                                : H[V(-q, -501)](Q, $)
                        )
                    );
                continue;
            case "7":
                return X[V(-U, -Z)]("");
        }
        break;
    }
}
var encrypt_mcr = (function (t) {
    var e = 67,
        r = 15,
        n = 164,
        o = 126,
        i = 137,
        a = 39,
        u = 176,
        s = 72,
        c = 56,
        l = 21,
        f = 35,
        p = 34,
        h = 35,
        d = 18,
        v = 25,
        g = 185,
        m = 1149,
        y = 744,
        w = 1295,
        _ = 1248,
        b = 1310,
        E = 1096,
        T = 1166,
        x = 1095,
        k = 1196,
        S = 1180,
        L = 1039,
        O = 976,
        R = 1347,
        I = 1117,
        A = 1168,
        C = 1233,
        N = 1157,
        P = 1006,
        B = 1122,
        F = 1277,
        j = 1288,
        M = 1271,
        D = 986,
        q = 162,
        U = {};
    function Z(t, e) {
        return a0_0x10f4ac(e, t - q);
    }
    (U[Z(-73, -66)] = function (t, e) {
        return t === e;
    }),
        (U[Z(e, 186)] = function (t, e) {
            return t < e;
        }),
        (U[Z(-r, -n)] = function (t, e) {
            return t ^ e;
        }),
        (U[Z(r, -o)] = function (t, e) {
            return t & e;
        }),
        (U[Z(-i, -a)] = function (t, e) {
            return t < e;
        }),
        (U[Z(-175, -u)] = function (t, e) {
            return t ^ e;
        }),
        (U[Z(-59, s)] = function (t, e) {
            return t ^ e;
        }),
        (U[Z(-c, -l)] = function (t, e) {
            return t >>> e;
        }),
        (U[Z(f, p)] = function (t, e) {
            return t >>> e;
        });
    for (
        var G, H, V = U, Y = 3988292384, W = 256, z = [];
        W--;
        z[W] = V[Z(h, -66)](G, 0)
    )
        for (H = 8, G = W; H--; )
            G = V[Z(r, d)](G, 1) ? V[Z(35, v)](G, 1) ^ Y : V[Z(h, g)](G, 1);
    return function (t) {
        function e(t, e) {
            return Z(e - 1181, t);
        }
        if (V[e(m, 1108)]((0, esm_typeof.Z)(t), e(y, 914))) {
            for (var r = 0, n = -1; V[e(w, _)](r, t[e(b, 1233)]); ++r)
                n = V[e(E, T)](
                    z[V[e(x, k)](n, 255) ^ t[e(S, L) + e(1022, O)](r)],
                    n >>> 8
                );
            return V[e(R, 1166)](n, -1) ^ Y;
        }
        for (r = 0, n = -1; V[e(I, 1044)](r, t[e(A, C)]); ++r)
            n = V[e(N, P)](
                z[V[e(1229, B)](V[e(F, k)](n, 255), t[r])],
                V[e(j, 1125)](n, 8)
            );
        return V[e(M, B)](V[e(D, 1122)](n, -1), Y);
    };
})();
function get_xs(api, data, a1) {
    if (data){
        api = api + JSON.stringify(data);
    }
    const md5 = crypto.createHash('md5');
    let x1 = md5.update(api).digest('hex');
    let x2 = "0|0|0|1|0|0|1|0|0|0|1|0|0|0|0|1|0|0|0";
    let x3 = a1;
    let x4 = Date.now();
    let x = `x1=${x1};x2=${x2};x3=${x3};x4=${x4};`;
    let payload = encrypt(btoa(x));
    let encrypt_data = {
        "signSvn":"54",
        "signType":"x2",
        "appId":"xhs-pc-web",
        "signVersion":"1",
        "payload":payload
    }
    encrypt_data = JSON.stringify(encrypt_data);
    encrypt_data = 'XYW_' + btoa(encrypt_data);
    return {
        'X-s': encrypt_data,
        'X-t': x4
    }
}

const fff = "I38rHdgsjopgIvesdVwgIC+oIELmBZ5e3VwXLgFTIxS3bqwErFeexd0ekncAzMFYnqthIhJeSfMDKutRI3KsYorWHPtGrbV0P9WfIi/eWc6eYqtyQApPI37ekmR1QL+5Ii6sdnoeSfqYHqwl2qt5B0DoIx+PGDi/sVtkIxdeTqwGtuwWIEhBIE3s3Mi3ICLdI3Oe0Vtl2ADmsLveDSJsSPw5IEvsiVtJOqw8BVwfPpdeTFWOIx4TIiu6ZPwbPut5IvlaLbgs3qtxIxes1VwHIkumIkIyejgsY/WTge7eSqte/D7sDcpipBKefm4sIx/efutZIE0ejutImcLj8fPHIx5e3ut3gIoe19kKIESPIhhgHgGUI38P4m+oIhLu/uwMI3qV2d3ejIgs6PwRIvge0fvejAR2IideTbVUqqwkIkOs196s6Y3eiVwopa/eDuwFICFeoBKsWqt1msoeYqtoIvIQIvm5muwGmPwJoei4KWKed77eiPwcIioejAAeVMDYIiNsWMvs3nV7Ikge1Vt6IkiIPqwwNqtUI3OeiVtdIkKsVqwVIENsDqtXNPwnsuwFIvGUI3HgGBIW2IveiPtMIhPKIi0eSPw4eY4KLa6sYjYdIirw4VtOZuw5ICKe3qtd+L/eTlJs1rSwIhOs3oNs3qts/VwqI3Ae0PwAIkge6sR+Ixds0UgsSPtRIh/eSPwUH0PwIiLpI33sxMgeka/ejFdsYPtQIiFFI3EYmutcICEIIEgs3SFSNsOsWutsIEbQmqtWGIKsjMveYPwrsPwZIvEDIhh+LuwtyPtbIC7eWMAs6Vt2ZVwHIiHQLPw5IvG4L9MgIEJe0L/sY9Ne3VwsHVt4I3HyIx0s6PtRIEKe0WPAI3bebW42ICSKIv0e1VwvbVww4VwFICb3IkJexfgskutTmI8lIC4LqPtseuteIxGiIibyIiT3IE/ekSKe3WLItuwKICLEpPwQrVwVIh6sT/lvIEm3sUNs0VwdcqwmzLYKr/DXIiMlaVwtIkdsDWY/IiTHrPwYIhZO2utfbPtwIEDIIClMICk/zVtjIE4OIiee6VtFLbV1IkbNI3gedo5ekPwkICYkIEPAnjHdIvpf/Wq9IxgedYoeSuwZIENsiVtQIEZ8IC3s0PtwIxIpzPtYI3ve1FTnouw6GuwQIx0eSPwwIEJsSDzSIEJsDoAsTVtrtsvsSuwOcm7e6utrIx/sxYJe3PtaIEq0Ikq2autQyMFnIv5sjVtap7Ks1LFEsuwNIxRPIivsdYYrIiAeDPtrIvHyIEgeWZFdIkHLIico8M8nICJeYWYFIkWMIvb9I3oeSdWLJuwzbuwynmgsdF5sfqtYIv6ejbNejqwzZVtNI3QPnqw0outHHqtUGqwEtVtWt06s6z5ei9/skl6e6uwqIiPGIhT6I3QFI3OsiBgsT7hUHVtGIEMEmut4P03ekPt8ICAsfZOefezZIvAsSqwmPpmxI36sfPt6IvesVuw7HqtyI3JefdDzOutZbc7ejph="
function XsCommon(a1, xs, xt) {
    let d = {
        s0: 5,
        s1: "",
        x0: "1",
        x1: "3.7.8-2",
        x2: "Windows",
        x3: "xhs-pc-web",
        x4: "4.26.0",
        x5: a1,
        x6: xt,
        x7: xs,
        x8: fff,
        x9: encrypt_mcr(xt.toString() + xs + fff),
        x10: 37,
    };
    let dataStr = JSON.stringify(d);
    return encrypt_b64Encode(encrypt_encodeUtf8(dataStr));
}

function get_request_headers_params(api, data, a1){
    api = 'url=' + api
    let xs_xt = get_xs(api, data, a1);
    let xs = xs_xt['X-s'];
    let xt = xs_xt['X-t'];
    let xs_common = XsCommon(a1, xs, xt);
    return {
        "xs": xs,
        "xt": xt,
        "xs_common": xs_common
    }
}
