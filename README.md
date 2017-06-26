![](http://onsi.github.io/ginkgo/images/ginkgo.png)

###<center> Ginkgo官方文档翻译
<p>
Ginkgo 是BDD(Behavior-Driver Development)类型的Golang测试框架，它可以帮助你编写写出富有表达力和容易理解的测试程序。该框架最好和Gomega匹配库配合使用。

本文档假设你会配合Ginkgo来使用Gomega，并且本文假设你对Go有一定的了解和在$GOPATH目录下Go如何组织包

---

##获取Ginkgo
使用go get 来获取：
```
 go get github.com/onsi/ginkgo/ginkgo
 go get github.com/onsi/gomega
```
这将会获取ginkgo，并且会在```$GOPATH/bin```目录下安装ginkgo可执行文件。

---
##开始：编写你的第一个测试
Ginkgo会钩入（hook into）Go已经存在的testing。这允许你使用```go test```来运行Ginkgo套件。
>这意味着Ginkgo可以和传统的Golang ```testing```共存。```go test```和```ginkgo```都可以运行你的所有测试套件。
###产生套件
为了为一个包编写Ginkgo测试，首先你**必须**生成一个Ginkgo测试套件。假设你有一个叫books的包：
```
cd path/to/books
ginkgo bootstrap
```
这会产生一个叫books_suite_test.go的文件，文件内容：
```
package books_test

import (
    . "github.com/onsi/ginkgo"
    . "github.com/onsi/gomega"
    "testing"
)

func TestBooks(t *testing.T) {
    RegisterFailHandler(Fail)
    RunSpecs(t, "Books Suite")
}
```
