-- phpMyAdmin SQL Dump
-- version 4.0.4
-- http://www.phpmyadmin.net
--
-- 主机: localhost
-- 生成日期: 2013 年 12 月 08 日 11:51
-- 服务器版本: 5.6.12-log
-- PHP 版本: 5.4.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- 数据库: `akbquiz`
--

-- --------------------------------------------------------

--
-- 表的结构 `memberinfo_group`
--

CREATE TABLE IF NOT EXISTS `memberinfo_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `groupname` varchar(8) NOT NULL,
  `founded` date NOT NULL,
  `description` longtext NOT NULL,
  `createtime` datetime NOT NULL,
  `edittime` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=11 ;

--
-- 转存表中的数据 `memberinfo_group`
--

INSERT INTO `memberinfo_group` (`id`, `groupname`, `founded`, `description`, `createtime`, `edittime`) VALUES
(2, 'AKB48', '2005-12-08', 'AKB48的名字取自东京的秋叶原地区（简称Akiba），并在秋叶原拥有名为AKB48剧场的专用表演场地，以“可以面对面的偶像”为理念，几乎每天都在专用剧场进行公演。另外，AKB48已被吉尼斯世界纪录认证为世界上最多成员的流行组合。', '2013-12-04 15:25:21', '2013-12-04 15:25:21'),
(3, 'SKE48', '2008-07-30', 'SKE48是由秋元康担任制作人，自2008年出道以东海地方为中心活动的日本女性偶像团体。与AKB48并不相同，成员主要出身于当地（特别是爱知县），且成员皆隶属同一事务所为其特征。日本唱片销量突破480万张。', '2013-12-04 15:26:34', '2013-12-04 15:26:34'),
(4, 'NMB48', '2010-10-09', 'NMB48是一个由秋元康担任制作人，以日本近畿地方为主要活动中心的女性偶像团体。2010年创立的NMB48是继SKE48之后，第二个根据AKB48的概念而创立的地方性姊妹团体，主要的幕后营运业者是以大阪为主要根据地的娱乐经济公司吉本兴业之合资企业京乐吉本（KYORAKU吉本.ホールディングス）。NMB48的团体名称源自位于大阪南区的闹区难波（其罗马拼音为“NAMBA”），大部分的成员都出身自近畿与中国地方一带的县。', '2013-12-04 15:27:19', '2013-12-04 15:27:19'),
(5, 'HKT48', '2011-10-23', 'HKT48是日本一个由作词家秋元康担任总制作人、以福冈市为主要活动据点的女子偶像组合，成立于2011年，团名源自福冈的古名博多（罗马拼音为HAKATA）。HKT48是继SKE48和NMB48之后，第三个依照AKB48的运作概念所成立的地方性姊妹组合，在福冈市中心的福冈海鹰城（Hawks Town）拥有专属表演剧场，大部分成员都出身自九州地方各县。', '2013-12-04 15:28:34', '2013-12-04 15:28:34'),
(6, 'NGZK46', '2011-08-22', '乃木坂46是作为AKB48的“官方对手”而成立的女子组合，因此跟AKB48的“姊妹组合”（如SKE48等）不同。例如组合不像AKB48及其姊妹组合般拥有AKB48剧场、NMB48剧场等专属表演场地。此外，据秋元康所讲，公演上半部份结束后，会由观众投票决定下半部份的编舞排位。组合名称中的“乃木坂”是唱片公司日本索尼音乐（SME）总部大楼的所在地。根据秋元康所说，“46”象征：“就算人数比AKB48少，也具有不逊于AKB48的干劲”。', '2013-12-04 15:29:50', '2013-12-04 15:56:43'),
(7, 'SDN48', '2009-08-01', 'SDN48是日本的女子偶像团体，以卖弄性感为特色，由秋元康于2009年创立。原则上每周六22时开始，于AKB48公演所使用的秋叶原AKB48剧场进行公演。2012年3月31日所有成员毕业之后，团体的活动事实上已完全终止。', '2013-12-04 15:33:38', '2013-12-04 15:33:38'),
(8, 'JKT48', '2013-02-16', 'JKT48是以印尼雅加达为中心活动的女子音乐组合。由秋元康担任制作人，是首支以日本以外作根据地的AKB48姊妹团体。', '2013-12-04 15:34:20', '2013-12-04 15:34:20'),
(9, 'SNH48', '2013-08-30', 'SNH48是一个在2012年于上海成立的中国大陆女子偶像团体，由秋元康担任总监督，为AKB48的姊妹团体。', '2013-12-04 15:35:04', '2013-12-04 15:35:04'),
(10, 'Unknown', '2013-12-08', '', '2013-12-08 08:01:23', '2013-12-08 08:01:23');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
