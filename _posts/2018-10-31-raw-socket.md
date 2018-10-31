---
layout: post
comments: true
title:  "Raw socket에 대하여 알아보자"
date:   2018-10-31 22:00:00 +0900
categories: network
description: Raw socket에 대하여 알아보자
---

> Raw(날 것의) Socket(네트워크 소켓)
>
> socket: 컴퓨터 네트워크를 경유하는 프로세스 간 통신의 종착점
>
> 오늘날 대부분은 인터넷 프로토콜(Internet Protocol; IP) 기반으로 하고 있으므로, 대부분의 네트워크 소켓은 **인터넷 소켓**이다.

네트워크는 osi 7계층으로 구성되어 있다.


> **OSI 7계층**
>
> | OSI/IP 모형                                                  |
> | ------------------------------------------------------------ |
> | 7. [응용 계층](https://ko.wikipedia.org/wiki/%EC%9D%91%EC%9A%A9_%EA%B3%84%EC%B8%B5) |
> | [NNTP](https://ko.wikipedia.org/wiki/NNTP)  · [SIP](https://ko.wikipedia.org/wiki/%EC%84%B8%EC%85%98_%EA%B0%9C%EC%8B%9C_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [SSI](https://ko.wikipedia.org/wiki/SSI)  · [DNS](https://ko.wikipedia.org/wiki/%EB%8F%84%EB%A9%94%EC%9D%B8_%EC%9D%B4%EB%A6%84_%EC%8B%9C%EC%8A%A4%ED%85%9C)  · [FTP](https://ko.wikipedia.org/wiki/%ED%8C%8C%EC%9D%BC_%EC%A0%84%EC%86%A1_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [고퍼](https://ko.wikipedia.org/wiki/%EA%B3%A0%ED%8D%BC_(%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C))  ·[HTTP](https://ko.wikipedia.org/wiki/HTTP)  · [NFS](https://ko.wikipedia.org/wiki/%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC_%ED%8C%8C%EC%9D%BC_%EC%8B%9C%EC%8A%A4%ED%85%9C)  · [NTP](https://ko.wikipedia.org/wiki/%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC_%ED%83%80%EC%9E%84_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [SMPP](https://ko.wikipedia.org/w/index.php?title=SMPP&action=edit&redlink=1)  · [SMTP](https://ko.wikipedia.org/wiki/%EA%B0%84%EC%9D%B4_%EC%9A%B0%ED%8E%B8_%EC%A0%84%EC%86%A1_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [DHCP](https://ko.wikipedia.org/wiki/DHCP) · [SNMP](https://ko.wikipedia.org/wiki/%EA%B0%84%EC%9D%B4_%EB%A7%9D_%EA%B4%80%EB%A6%AC_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [텔넷](https://ko.wikipedia.org/wiki/%ED%85%94%EB%84%B7)  · [(더 보기)](https://ko.wikipedia.org/wiki/%EB%B6%84%EB%A5%98:%EC%9D%91%EC%9A%A9_%EA%B3%84%EC%B8%B5_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C) |
> | 6. [표현 계층](https://ko.wikipedia.org/wiki/%ED%91%9C%ED%98%84_%EA%B3%84%EC%B8%B5) |
> | [MIME](https://ko.wikipedia.org/wiki/MIME)  · [XDR](https://ko.wikipedia.org/wiki/XDR)  · [TLS](https://ko.wikipedia.org/wiki/%EC%A0%84%EC%86%A1_%EA%B3%84%EC%B8%B5_%EB%B3%B4%EC%95%88)  · [SSL](https://ko.wikipedia.org/wiki/SSL) |
> | 5. [세션 계층](https://ko.wikipedia.org/wiki/%EC%84%B8%EC%85%98_%EA%B3%84%EC%B8%B5) |
> | [지명 파이프](https://ko.wikipedia.org/wiki/%EC%A7%80%EB%AA%85_%ED%8C%8C%EC%9D%B4%ED%94%84)  · [넷바이오스](https://ko.wikipedia.org/wiki/%EB%84%B7%EB%B0%94%EC%9D%B4%EC%98%A4%EC%8A%A4)  · [SAP](https://ko.wikipedia.org/wiki/SAP) |
> | 4. [전송 계층](https://ko.wikipedia.org/wiki/%EC%A0%84%EC%86%A1_%EA%B3%84%EC%B8%B5) |
> | [TCP](https://ko.wikipedia.org/wiki/%EC%A0%84%EC%86%A1_%EC%A0%9C%EC%96%B4_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [UDP](https://ko.wikipedia.org/wiki/%EC%82%AC%EC%9A%A9%EC%9E%90_%EB%8D%B0%EC%9D%B4%ED%84%B0%EA%B7%B8%EB%9E%A8_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [SCTP](https://ko.wikipedia.org/wiki/%EC%8A%A4%ED%8A%B8%EB%A6%BC_%EC%A0%9C%EC%96%B4_%EC%A0%84%EC%86%A1_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [DCCP](https://ko.wikipedia.org/wiki/%EB%8D%B0%EC%9D%B4%ED%84%B0%EA%B7%B8%EB%9E%A8_%ED%98%BC%EC%9E%A1_%EC%A0%9C%EC%96%B4_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C) |
> | 3. [네트워크 계층](https://ko.wikipedia.org/wiki/%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC_%EA%B3%84%EC%B8%B5) |
> | [ARP](https://ko.wikipedia.org/wiki/%EC%A3%BC%EC%86%8C_%EA%B2%B0%EC%A0%95_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [IP](https://ko.wikipedia.org/wiki/%EC%9D%B8%ED%84%B0%EB%84%B7_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [ICMP](https://ko.wikipedia.org/wiki/%EC%9D%B8%ED%84%B0%EB%84%B7_%EC%A0%9C%EC%96%B4_%EB%A9%94%EC%8B%9C%EC%A7%80_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [IPsec](https://ko.wikipedia.org/wiki/IPsec)  · [IGMP](https://ko.wikipedia.org/wiki/%EC%9D%B8%ED%84%B0%EB%84%B7_%EA%B7%B8%EB%A3%B9_%EA%B4%80%EB%A6%AC_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [IPX](https://ko.wikipedia.org/wiki/IPX)  · [애플토크](https://ko.wikipedia.org/wiki/%EC%95%A0%ED%94%8C%ED%86%A0%ED%81%AC) |
> | 2. [데이터 링크 계층](https://ko.wikipedia.org/wiki/%EB%8D%B0%EC%9D%B4%ED%84%B0_%EB%A7%81%ED%81%AC_%EA%B3%84%EC%B8%B5) |
> | [CSLIP](https://ko.wikipedia.org/w/index.php?title=CSLIP&action=edit&redlink=1)  · [SLIP](https://ko.wikipedia.org/w/index.php?title=SLIP&action=edit&redlink=1)  · [이더넷](https://ko.wikipedia.org/wiki/IEEE_802.3)  · [프레임 릴레이](https://ko.wikipedia.org/wiki/%ED%94%84%EB%A0%88%EC%9E%84_%EB%A6%B4%EB%A0%88%EC%9D%B4)  · [ITU-T G.hn DLL](https://ko.wikipedia.org/w/index.php?title=G.hn&action=edit&redlink=1)  · [L2TP](https://ko.wikipedia.org/w/index.php?title=L2TP&action=edit&redlink=1)  · [PPP](https://ko.wikipedia.org/wiki/%EC%A0%90%EB%8C%80%EC%A0%90_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C)  · [PPTP](https://ko.wikipedia.org/w/index.php?title=PPTP&action=edit&redlink=1) |
> | 1. [물리 계층](https://ko.wikipedia.org/wiki/%EB%AC%BC%EB%A6%AC_%EA%B3%84%EC%B8%B5) |
> | [RS-232](https://ko.wikipedia.org/wiki/RS-232)  · [RS-449](https://ko.wikipedia.org/w/index.php?title=RS-449&action=edit&redlink=1)  · [RS-485](https://ko.wikipedia.org/wiki/RS-485)  · [V.35](https://ko.wikipedia.org/w/index.php?title=V.35&action=edit&redlink=1)  · [V.34](https://ko.wikipedia.org/w/index.php?title=V.34&action=edit&redlink=1)  ·[I.430](https://ko.wikipedia.org/w/index.php?title=I.430&action=edit&redlink=1)  ·[I.431](https://ko.wikipedia.org/w/index.php?title=I.431&action=edit&redlink=1)  · [T1](https://ko.wikipedia.org/w/index.php?title=T1_(%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%82%B9)&action=edit&redlink=1)  · [E1](https://ko.wikipedia.org/w/index.php?title=E-carrier&action=edit&redlink=1)  · [POTS](https://ko.wikipedia.org/w/index.php?title=POTS&action=edit&redlink=1)  · [SONET/SDH](https://ko.wikipedia.org/w/index.php?title=SONET/SDH&action=edit&redlink=1)  · [OTN](https://ko.wikipedia.org/w/index.php?title=%EA%B4%91_%EC%A0%84%EC%86%A1_%ED%94%84%EB%A1%9C%ED%86%A0%EC%BD%9C&action=edit&redlink=1) · [DSL](https://ko.wikipedia.org/wiki/DSL)  · [802.11a/b/g/n PHY](https://ko.wikipedia.org/wiki/IEEE_802.11)  · [ITU-T G.hn PHY](https://ko.wikipedia.org/w/index.php?title=G.hn&action=edit&redlink=1)  · [이더넷](https://ko.wikipedia.org/w/index.php?title=%EC%9D%B4%EB%8D%94%EB%84%B7_%EB%AC%BC%EB%A6%AC_%EA%B3%84%EC%B8%B5&action=edit&redlink=1)  · [USB](https://ko.wikipedia.org/wiki/USB)  · [블루투스](https://ko.wikipedia.org/wiki/%EB%B8%94%EB%A3%A8%ED%88%AC%EC%8A%A4) |
>
> 각 계층은 하위 계층의 기능만을 이용하며, 상위 계층에게 기능을 제공한다.
>
> 즉 상위 계층은 하위계층을 이용할 수 있으며, 하위계층은 상위계층을 이용할 수  없다.

Raw socket은 인터넷 프로토콜 패킷을 주고받게 해주는 소켓이다.

보통 socket은 TCP/IP 헤더가 만들어져 있으며 운영체제의 커널단에서 프로토콜에 맞는 default 값을  채워서 제공한다.

이런 헤더를 직접적으로 조절할 수 있는 socket을 raw socket이라고 한다.

**Raw Socket의 특징**

- 네트워크 계층(3 layer) 위로 모두 접근이 가능하다.
- 네트워크 계층 헤더와 전송 계층 헤더를 직접 제어(프로그래밍) 가능하다.
- 네트워크 계층으로 전송되는 모든 패킷을 모니터링 및 감지 가능하다.
- IP segment에서 암호화된 악성코드가 있는 경우에 문제가 발생할 수 있다.
- root 권한에서만 사용할 수 있다.

![img](https://player.slidesplayer.org/61/11291176/slides/slide_7.jpg)

출처: [TCP/IP 윈도우 소켓 프로그래밍](https://slidesplayer.org/slide/11291176/)

위의 영역들을 직접 프로그래밍하여 값을 채워 넣을 수 있다.

우리가 사용하는 네트워크는 0과 1로 표현 가능한(2진수로 된) 주파수들의 흐름으로 이루어져 있다.

이런 주파수의 데이터 단위를 패킷이라고 부른다.  [좀더 자세한 설명영상](https://www.youtube.com/watch?v=XaGXPObx2Gs&t=0s&list=PLowKtXNTBypH19whXTVoG3oKSuOcw_XeW&index=2)

실제로 인터넷 선이 연결된 곳(무선도 결국 공유기가 인터넷 선으로 보냄)에서 발생하는 데이터들은 주파수로 변하여 송수신되며, raw socket을 이용하면 주파수들을 모두 들여다 볼 수 있다.

a라는 출발지에서 d라는 목적지까지 가는 경로에 b, c가 존재한다면 b와 c을 반드시 지나간다. 즉, 내 정보는 인터넷에 연결된 순간 사방에 공유된다.

