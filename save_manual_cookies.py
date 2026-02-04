
import json

cookies = {}
raw_text = """
__Secure-1PAPISID	n5lch8eF5FS820BB/AvluuoNzDUl9IPqNk	.google.com	/	2027-03-05T02:20:10.585Z	51		✓				High
__Secure-1PSID	g.a0006Qi9MUa1yBFgintbYTR_d6Ooy5z4tHRtzhwm2-aj_EusAvrkwoVeiQBmxI0gTyWQkNJULAACgYKAWUSARASFQHGX2MiiyOcL5a53cZRq3B0TB2WMhoVAUF8yKpaw5Lsyuk95IR4xum8EMcd0076	.google.com	/	2027-03-05T02:20:10.585Z	167	✓	✓				High
__Secure-1PSIDCC	AKEyXzVmF5ZoVcT6HtUpaOx785ycrCijMs5QI7tuoDaVfWADULQ21tUU4lJHpPy7oayIAWdPLA	.google.com	/	2027-02-04T07:34:19.321Z	90	✓	✓				High
__Secure-1PSIDRTS	sidts-CjYB7I_69PUahPh3POLb6kfJnK8M09ojBmnDY3lRZBc4dHR5IqHtbdgZNLBnJVbZDyZmsDfdpG4QAA	.google.com	/	2026-02-04T07:43:03.068Z	101	✓	✓				High
__Secure-1PSIDTS	sidts-CjYB7I_69PUahPh3POLb6kfJnK8M09ojBmnDY3lRZBc4dHR5IqHtbdgZNLBnJVbZDyZmsDfdpG4QAA	.google.com	/	2027-02-04T07:33:03.068Z	100	✓	✓				High
__Secure-3PAPISID	n5lch8eF5FS820BB/AvluuoNzDUl9IPqNk	.google.com	/	2027-03-05T02:20:10.586Z	51		✓	None			High
__Secure-3PSID	g.a0006Qi9MUa1yBFgintbYTR_d6Ooy5z4tHRtzhwm2-aj_EusAvrkemnEOrxBMChvv3vkcKTSxQACgYKAQISARASFQHGX2MiQp9HS-9TjP6QFTlgwFztqxoVAUF8yKqubgKPgn_qnQolr1ZxUG230076	.google.com	/	2027-03-05T02:20:10.585Z	167	✓	✓	None			High
__Secure-3PSIDCC	AKEyXzWzw1v5zc6-v-ifWt2PR0LlWWi1WUwwWjf1NBt6MDzaVG5DBhn8SK1z-1FqQmyb-N0bXDk	.google.com	/	2027-02-04T07:34:19.321Z	91	✓	✓	None			High
__Secure-3PSIDRTS	sidts-CjYB7I_69PUahPh3POLb6kfJnK8M09ojBmnDY3lRZBc4dHR5IqHtbdgZNLBnJVbZDyZmsDfdpG4QAA	.google.com	/	2026-02-04T07:43:03.068Z	101	✓	✓	None			High
__Secure-3PSIDTS	sidts-CjYB7I_69PUahPh3POLb6kfJnK8M09ojBmnDY3lRZBc4dHR5IqHtbdgZNLBnJVbZDyZmsDfdpG4QAA	.google.com	/	2027-02-04T07:33:03.068Z	100	✓	✓	None			High
__Secure-BUCKET	CLEG	.google.com	/	2026-07-28T02:18:54.199Z	19	✓	✓				Medium
__Secure-OSID	g.a0006Qi9MR1DC-MpC1PTa3MeJZTMthq1x0lLkf4VCjEYXw-ZNmpFXXYtRSiNYMLO_jtvc2SiJAACgYKAbUSARASFQHGX2MirWTQaVzyJySl81E4WnXKRRoVAUF8yKqVgQIBV9zDPUp1yRoRb9y70076	play.google.com	/	2027-03-05T02:26:09.953Z	166	✓	✓	None			Medium
__Secure-OSID	g.a0006Qi9MQT6i8ZQ-fOLlsS303DADQHgLhWLdxc8DCH4c0X0yhhLAswn_Im79UV7T3umifKSjwACgYKAaUSARASFQHGX2MimpwXG89UtsPtU9JI4KJJzxoVAUF8yKp8MWjRr66PhjGbDsuO9BEH0076	notebooklm.google.com	/	2027-03-05T22:54:32.228Z	166	✓	✓				Medium
_ga	GA1.1.102226860.1770190389	.notebooklm.google.com	/	2027-03-11T07:33:11.712Z	29						Medium
_ga_W0LDH41ZCB	GS2.1.s1770190389$o1$g1$t1770190392$j57$l0$h0	.notebooklm.google.com	/	2027-03-11T07:33:12.125Z	59						Medium
_gcl_au	1.1.485505991.1769727274	.notebooklm.google.com	/	2026-04-29T22:54:34.000Z	31						Medium
AEC	AaJma5u0qxlt_CUv818lx4Ay2FpaA6ipaHzut7quIPtKJsxbo3CdnDv8GQ	.google.com	/	2026-07-28T02:18:55.118Z	61	✓	✓	Lax			Medium
APISID	CpWMsfXk28datbFw/Aky9aaj4S1426n8E9	.google.com	/	2027-03-05T02:20:10.585Z	40						High
HSID	AujKrBLkwXoZOpnd6	.google.com	/	2027-03-05T02:20:10.585Z	21	✓					High
NID	528=ZOhk5cf09TC_thuDpzJRJRn9xkIskhz7euXlSxb5ckGqcGo2wJwIYpcMouf-OJvo1rjOgLt4ApxZ0GnxodSMpoTNTaUeoI3Pt5c_iFqFJyb6lFAMoTtuBuWVeiKfCsqVOOXi3bt_rLpd_T-XpEe6tu_NH73IHr9fW2qv59433GpJw_prE5lVu4uViBoiKho1jO8KuY2ynmIaxvMuu-54XfEyXWp8Mlv-s-07bZUIIIDWnyd5j8yuJzoyWhltpRvUuOkeeB6iVskurgJRJT1DYtmW7B2keAHqLKMYRc2xPwQdLZymNZbr1l68_pOZtuzsgWLLJPdOhpiG_t712e4fupw1YdfFUnjPeo6iKYmY5raaw2Ibwd9BVlT8OW5l1jM8mYH07GW2c68kcj-VfT03uBb2wyJr6KW6AR54sCY2N8U_lmnvRBOvpt2KQlBrtUfK-F1H8vqNWQ7gcKSqWqNFjjJsVmTj24gkQ_ABbg79zv8gnfZJHP1KlE_rsoK0flC8C7Ay0-8siArmYZ_hlfvJMxPmrlVLcd3vedj-zSS5RGN-hgLeMMAo393A46lgBjh8pnNsj9RE9crWs9NTNmtZL8qImxlFKQfgOMpRXZfadxx77ja_d9Qi_a0de3rICoQfgo-h7tzX5WUgMtSOyHLS250-L5eR6-2SpDqJbxdE5VH1EJNoxy2O_AFn60j27AQe_8z8RrOQXg3V6e3UlK3TMMkEWL99L0YqemiTHo0CXM-mI11HgU8LXvRAUOg3VJOLe4A95DojpFpENwTGddcPaVaKSWEVwc9WXDsdBWJIWhSz7JfSkWQ8uU4-WeNNCz6AWXbDsF8-QPENU6awAEJzXVNeFbqXn0d_hJs9G3ANjSAnRpr8Dzd0OYum4ZD8lyosTZOlu_ZIKLsz8JmdFBvWrv_W66A_MTlTnxuSg-549liwEUMoM71O-e_o33teLaGp7OkzL7OXss5s4XWsM81EROLBGUh6Mgs_GPmbk0Ra2bBhPPzhXg3lhvfVqI_AqunDFjNZU7vsryNcg_bnzW7F_97MiCHK0xM5BEcft37dkOCOWjEq3xlW4DBBpIlox_oMce3wc0c	.google.com	/	2026-08-06T00:50:42.940Z	1102	✓	✓	None			Medium
OSID	g.a0006Qi9MR1DC-MpC1PTa3MeJZTMthq1x0lLkf4VCjEYXw-ZNmpFIpuHM_OLFQkBSkFIWOCErwACgYKARYSARASFQHGX2MiTaCNhfC9ZNpkHOWKD0B-BxoVAUF8yKp-BqgQdswGZNurW2GZMBdl0076	play.google.com	/	2027-03-05T02:26:09.953Z	157	✓	✓				Medium
OSID	g.a0006Qi9MQT6i8ZQ-fOLlsS303DADQHgLhWLdxc8DCH4c0X0yhhLKZfG8NzewIBbJWxoqGIMjgACgYKAUISARASFQHGX2MiHDcF93Ha1f0y1WlV4is3-RoVAUF8yKqxbSdfygZPbC_dI85ya7Wn0076	notebooklm.google.com	/	2027-03-05T22:54:32.228Z	157	✓	✓				Medium
SAPISID	n5lch8eF5FS820BB/AvluuoNzDUl9IPqNk	.google.com	/	2027-03-05T02:20:10.585Z	41		✓				High
SEARCH_SAMESITE	CgQIhqAB	.google.com	/	2026-08-01T08:59:19.915Z	23			Strict			Medium
SID	g.a0006Qi9MUa1yBFgintbYTR_d6Ooy5z4tHRtzhwm2-aj_EusAvrkQyi7nnBLaFz6SZdh_a0ffQACgYKAVASARASFQHGX2MiUqAT-tUWeJRaCtgxoZUuEBoVAUF8yKr1__w1cCn7WgWOW7ad2Mbn0076	.google.com	/	2027-03-05T02:20:10.585Z	156						High
SIDCC	AKEyXzX5XL3--OoxnAb2hlh2w3jFu9UPjs9YmxVmoQWicaCmrhbG3vWXScpU9yBb6DaBtEAucw	.google.com	/	2027-02-04T07:34:19.320Z	79						High
SSID	AG1Xm-AYMRnu6gwJj	.google.com	/	2027-03-05T02:20:10.585Z	21	✓	✓				High
"""

# 간단한 파싱: 탭으로 구분된 데이터에서 이름과 값은 보통 첫 번째, 두 번째 컬럼이거나 포맷에 따라 다름
# 사용자가 준 포맷은 "이름 \t 값 \t 도메인 ..." 형태임

for line in raw_text.strip().split('\n'):
    parts = line.split('\t')
    if len(parts) >= 2:
        name = parts[0].strip()
        value = parts[1].strip()
        if name and value:
            cookies[name] = value

with open("auth_cookies.json", "w") as f:
    json.dump(cookies, f)

print(f"✅ {len(cookies)}개의 쿠키를 저장했습니다.")
