
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `Arcadia`
--

-- --------------------------------------------------------

--
-- Table structure for table `badwords`
--

CREATE TABLE IF NOT EXISTS `badwords` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `words` varchar(100) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=5 ;

--
-- Dumping data for table `badwords`
--

INSERT INTO `badwords` (`ID`, `words`) VALUES
(1, 'gosh'),
(2, 'fuck'),
(3, 'shit'),
(4, 'testbadword');

-- --------------------------------------------------------

--
-- Table structure for table `matches`
--

CREATE TABLE IF NOT EXISTS `matches` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `matches` varchar(30) DEFAULT NULL,
  `response` varchar(120) DEFAULT NULL,
  KEY `ID` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 AUTO_INCREMENT=1 ;

-- --------------------------------------------------------

--
-- Table structure for table `responses`
--

CREATE TABLE IF NOT EXISTS `responses` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `message` varchar(30) NOT NULL,
  `response` varchar(400) NOT NULL,
  PRIMARY KEY (`id`,`message`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=58 ;

--
-- Dumping data for table `responses`
--

INSERT INTO `responses` (`id`, `message`, `response`) VALUES
(1, 'ping', 'pong'),
(2, 'I acci', 'I accidentally build shelf'),
(3, '!op', 'not enabled'),
(4, '!deop', 'Not enabled'),
(5, '!kick', 'Not enabled'),
(6, '!ban', 'Not enabled'),
(7, '!discoparty', ' *plays tunes*|| *starts dancing* || Come on everybody its the hampster dance!'),
(8, '!hiwizard', 'wizard, |names| would like to welcome you :D'),
(9, '!rickroll', 'Never gonna give you up. Never gonna let you down.'),
(10, '!easter', '*Chucks eggs at: |names| ha! '),
(11, '!sleep', 'Sleep is for wimps!'),
(12, '!good', '|action|Gives Bart a Mountain Dew Voltage'),
(13, '!whee', 'Yeah ha! *jumps down the water slide* WHEEEE!!!!'),
(14, '!mdsmith2', 'o_0'),
(15, '!violet', ':P'),
(16, '!purple', 'You are funny |nick|... you actually want me to respond to purple?'),
(17, '!grapefruit', '|nick|, you are the most awesome person ever... just saying <3'),
(18, '!ben', 'The force is strong with this one'),
(19, '!harrison', '|action| pats harrison on the head XD'),
(20, '!monday', 'I can''t wait till Friday.'),
(21, '!tuesday', 'I can''t wait till Friday.'),
(22, '!wednesday', 'I can''t wait till Friday.'),
(23, '!thursday', 'Almost there!'),
(24, '!friday', 'It''s Friday, Friday. Gotta getdown on Friday. :D'),
(25, '!secret', '|action|tackles lester'),
(26, '!gps', 'Recalculating!'),
(27, '!Christmas', '*Pours EggNog on : |names| ha! :P Merry Christmas.'),
(28, '!bunny', '(bunny)!!!'),
(29, '!pirate', '|action| puts on an eyepatch and swings a cutless around || Arrr!!!'),
(30, '!sandwich', 'Hobbit wants a sandwich!'),
(31, '!sandvich', 'In Soviet Russia, the Sandvich eats YOU!'),
(32, '!hidden', 'Other commands: !hiwizard,!easter, !sleep, !good, !whee, # !mdsmith2, !violet, !purple, !batman, !grapefruit, !ben, !friday, !secret, !gps, !christmas. !bunny, !monday, !pirate, 
!sandwich, !sandvich'),
(33, '!caturday', ':3'),
(34, 'squirrel', 'Squirrel... WHERE?!!!!'),
(35, '!test', 'SAJOIN |nick| #test'),
(36, '..how are you?', 'Nailed it!'),
(37, '!mole', 'There is a mole in our midst. geo is working hard to locate it. 0_o'),
(38, '!grandma', '(grandma)!!'),
(39, 'I''m from Canada', 'I''m sorry.'),
(40, '!mater', 'mater is having his moment.'),
(41, '!4th', '*Chucks water balloons at: |names|  Happy Independence Day! :D God Bless America!  *Launches fireworks*'),
(42, '.die', '/kick |nick| haha.. no.'),
(43, '!translate', '翻訳サーバー エラー'),
(44, '!sajoin', '/quote sajoin Bart_Roberts #main'),
(45, '!joinbart', 'SAJOIN Bart_Roberts #main'),
(46, '!boss', 'Captain_Harlock is the boss.'),
(47, '!hi', 'Hey!'),
(49, 'Arcadia, make me a sandwich', 'no'),
(51, 'Arcadia make me a sandwich', 'no'),
(53, 'Arcadia, sudo make me a sandwi', 'Okay *makes sandwich*'),
(54, 'marco', 'polo!'),
(55, 'marko', 'Polo!'),
(56, 'Marco!', 'Polo!'),
(57, '!rules', 'http://christianlifefm.com/chatrules.php');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

