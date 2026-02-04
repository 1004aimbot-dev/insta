
import json
import browser_cookie3

raw_cookies = """
__Secure-1PAPISID	n5lch8eF5FS820BB/AvluuoNzDUl9IPqNk	.google.com	/	2027-03-05T02:20:10.585Z	51		✓				High
__Secure-1PSID	g.a0006Qi9MUa1yBFgintbYTR_d6Ooy5z4tHRtzhwm2-aj_EusAvrkwoVeiQBmxI0gTyWQkNJULAACgYKAWUSARASFQHGX2MiiyOcL5a53cZRq3B0TB2WMhoVAUF8yKpaw5Lsyuk95IR4xum8EMcd0076	.google.com	/	2027-03-05T02:20:10.585Z	167	✓	✓				High
__Secure-1PSIDCC	AKEyXzXzD8ZrbJRgqD-NqU2uIEsz7PM_kLRKAxB8XNkC85u3pbm9AGzTae2jsRdxiXaG96evOg	.google.com	/	2027-02-04T11:16:54.713Z	90	✓	✓				High
__Secure-1PSIDRTS	sidts-CjYB7I_69KPqUgShWxqHgJw21ucqNsI28T42nXuQTbTen7lkLZoylhRUTrB3nI1f9-mf6qZE5XcQAA	.google.com	/	2026-02-04T11:21:23.475Z	101	✓	✓				High
__Secure-1PSIDTS	sidts-CjYB7I_69KPqUgShWxqHgJw21ucqNsI28T42nXuQTbTen7lkLZoylhRUTrB3nI1f9-mf6qZE5XcQAA	.google.com	/	2027-02-04T11:11:23.474Z	100	✓	✓				High
__Secure-3PAPISID	n5lch8eF5FS820BB/AvluuoNzDUl9IPqNk	.google.com	/	2027-03-05T02:20:10.586Z	51		✓	None			High
__Secure-3PSID	g.a0006Qi9MUa1yBFgintbYTR_d6Ooy5z4tHRtzhwm2-aj_EusAvrkemnEOrxBMChvv3vkcKTSxQACgYKAQISARASFQHGX2MiQp9HS-9TjP6QFTlgwFztqxoVAUF8yKqubgKPgn_qnQolr1ZxUG230076	.google.com	/	2027-03-05T02:20:10.585Z	167	✓	✓	None			High
__Secure-3PSIDCC	AKEyXzWfOWNOv31wvA9Q6u00enMvvDr6dWTgP11zDNk4ArNs0_oNYHr_hy9S90leVQbIbV_RJcw	.google.com	/	2027-02-04T11:16:54.714Z	91	✓	✓	None			High
__Secure-3PSIDRTS	sidts-CjYB7I_69KPqUgShWxqHgJw21ucqNsI28T42nXuQTbTen7lkLZoylhRUTrB3nI1f9-mf6qZE5XcQAA	.google.com	/	2026-02-04T11:21:23.475Z	101	✓	✓	None			High
__Secure-3PSIDTS	sidts-CjYB7I_69KPqUgShWxqHgJw21ucqNsI28T42nXuQTbTen7lkLZoylhRUTrB3nI1f9-mf6qZE5XcQAA	.google.com	/	2027-02-04T11:11:23.475Z	100	✓	✓	None			High
__Secure-BUCKET	CLEG	.google.com	/	2026-07-28T02:18:54.199Z	19	✓	✓				Medium
__Secure-OSID	g.a0006Qi9MR1DC-MpC1PTa3MeJZTMthq1x0lLkf4VCjEYXw-ZNmpFXXYtRSiNYMLO_jtvc2SiJAACgYKAbUSARASFQHGX2MirWTQaVzyJySl81E4WnXKRRoVAUF8yKqVgQIBV9zDPUp1yRoRb9y70076	play.google.com	/	2027-03-05T02:26:09.953Z	166	✓	✓	None			Medium
__Secure-OSID	g.a0006Qi9MfZesP1uPVObENjp2RCeNoq8MQf_RMx7mnwXA3DBOqxSLNkMD9GcXajzyXg-c0OrZwACgYKAbESARASFQHGX2MiaNSZgAyqBSmyKb5VXIjixRoVAUF8yKpOaXWaLYnexAgXnL3YcvnD0076	notebooklm.google.com	/	2027-03-11T11:16:31.141Z	166	✓	✓				Medium
_ga	GA1.1.102226860.1770190389	.notebooklm.google.com	/	2027-03-11T11:16:33.039Z	29						Medium
_ga_W0LDH41ZCB	GS2.1.s1770203532$o2$g1$t1770203806$j47$l0$h0	.notebooklm.google.com	/	2027-03-11T11:16:46.877Z	59						Medium
_gcl_au	1.1.485505991.1769727274	.notebooklm.google.com	/	2026-04-29T22:54:34.000Z	31						Medium
AEC	AaJma5u0qxlt_CUv818lx4Ay2FpaA6ipaHzut7quIPtKJsxbo3CdnDv8GQ	.google.com	/	2026-07-28T02:18:55.118Z	61	✓	✓	Lax			Medium
APISID	CpWMsfXk28datbFw/Aky9aaj4S1426n8E9	.google.com	/	2027-03-05T02:20:10.585Z	40						High
HSID	AujKrBLkwXoZOpnd6	.google.com	/	2027-03-05T02:20:10.585Z	21	✓					High
NID	528=kLpWddpHOqMNOY6WD5wVHBTcPxe4CAj6NeG62ZMW2GA2xbsJEIVwT6gcGrWIt62hvym-ZJZeDFMZJ8hDV3g3027WOkrn3MjQ8m-ZhyrcwqnPlcsmCc9-tAK9_qfSzjl7PtEgoPpsp-3jZDh8GZH7No1tbsFy0gUUy71b38Y6vRUzDOvKajPC3EMRyBQMv-5CNqGph2MpwMolGbcIATebfCFDoDpVTiAgKtLZCs9JQa3n7laS-A2E6EjCuGB3P8D-GZ-9MW3FWJIP3FM21zFim9CwV-_EWsF8CAl2T8Tc2KP4zzaW3_pMQEPLXemm8HuNPFdkgMd9LhEiHziHEO4TRL8jRWwX8LF39O3MCfZUQtZi9lrFBG5VV_kwBluHXfHsjBkBBKgsLeany_Dnj5CF0B5DFVDpkc7KubkoWXQLlcJdBNmsVLhX7RjCQu4LvyHNsmi5ctru-w9gb1HcGhHVTycmjW5X9cuPldqKCjW8KiBPON_6kfFMBUyDHpbFAwhlmlVPsSQJsav0J62iIyneRA-bLJVnS77XFV2fAiUECPyWeBiWsAmZw1enZyz4g2BD9dFyDgNW8cpWiGFyid29nI-FPSS4JuDbUq507nGG2mPYwn_elmlsFCuiLNhmJLpD6QphP0xQBJ1qlNR0WWiG783w04vV70ug1EQZRqefunBMiXevKYo4jXrOhlXYdHgf1uXj3hPkVOTTuFqbcRTG_EK5uVakMr9T8quxA5-_SZ0OPeqS-IRHiEusJzXv_zuKRX_4S3CGlw_lLPASHZGK3yassLtkM2-TI6sZqMS1IQiHquYRIim4fGPVhfkPKqF44NWnhQnhI1F_lneFiorbVjYDXHSG1w6HTNrzEnJ74BcXxFqcYQm3sztCvMnzX90WAj4TpE0Az0V1N0cyPmKbRT8M4IPj5JOYeKOqI2GmtR79AsHTCRW3KLtmRcbJQcLJyrI3vimjoUZP58itJ-RwD3TPSOGz1GbdIf-y0L-fNCHYAlC7lIOg55F2V502XkWpCkT_01gscOKd6k8T96rtEyBysJgoo75Ejej7otGwCWmyDR3UTnETkcZwy3fStBxt-uYxR2M	.google.com	/	2026-08-06T00:50:42.606Z	1102	✓	✓	None			Medium
OSID	g.a0006Qi9MR1DC-MpC1PTa3MeJZTMthq1x0lLkf4VCjEYXw-ZNmpFIpuHM_OLFQkBSkFIWOCErwACgYKARYSARASFQHGX2MiTaCNhfC9ZNpkHOWKD0B-BxoVAUF8yKp-BqgQdswGZNurW2GZMBdl0076	play.google.com	/	2027-03-05T02:26:09.953Z	157	✓	✓				Medium
OSID	g.a0006Qi9MfZesP1uPVObENjp2RCeNoq8MQf_RMx7mnwXA3DBOqxSDvl586mDgyN8xvwv5BWDZAACgYKASYSARASFQHGX2MiYm3iKPQSoWMvmHrxvDDZMhoVAUF8yKrft_bNbgzB6wKlaY9Ab1IO0076	notebooklm.google.com	/	2027-03-11T11:16:31.141Z	157	✓	✓				Medium
SAPISID	n5lch8eF5FS820BB/AvluuoNzDUl9IPqNk	.google.com	/	2027-03-05T02:20:10.585Z	41		✓				High
SEARCH_SAMESITE	CgQIhqAB	.google.com	/	2026-08-01T08:59:19.915Z	23			Strict			Medium
SID	g.a0006Qi9MUa1yBFgintbYTR_d6Ooy5z4tHRtzhwm2-aj_EusAvrkQyi7nnBLaFz6SZdh_a0ffQACgYKAVASARASFQHGX2MiUqAT-tUWeJRaCtgxoZUuEBoVAUF8yKr1__w1cCn7WgWOW7ad2Mbn0076	.google.com	/	2027-03-05T02:20:10.585Z	156						High
SIDCC	AKEyXzWfyyjJzC_R9-2TC8lna7KAi-5KRFoq8bellptpD4QTQfPAH-Bfdh6dPORxtSUC8kE3fA	.google.com	/	2027-02-04T11:16:54.713Z	79						High
SSID	AG1Xm-AYMRnu6gwJj	.google.com	/	2027-03-05T02:20:10.585Z	21	✓	✓				High
"""

def parse_and_save():
    cookies = {}
    for line in raw_cookies.strip().split('\n'):
        parts = line.split('\t')
        if len(parts) >= 2:
            name = parts[0].strip()
            value = parts[1].strip()
            cookies[name] = value

    with open('auth_cookies.json', 'w') as f:
        json.dump(cookies, f, indent=4)
    print(f"✅ {len(cookies)}개의 쿠키가 저장되었습니다.")

if __name__ == "__main__":
    parse_and_save()
