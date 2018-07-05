-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 05 Lip 2018, 22:03
-- Wersja serwera: 10.1.30-MariaDB
-- Wersja PHP: 7.2.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Baza danych: `takethesurvey`
--

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `completedanswers`
--

CREATE TABLE `completedanswers` (
  `id_completedanswer` int(11) NOT NULL,
  `id_completedsurvey` int(11) NOT NULL,
  `id_surveytemplate` int(11) NOT NULL,
  `id_question` int(11) NOT NULL,
  `id_answer` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `completedanswers`
--

INSERT INTO `completedanswers` (`id_completedanswer`, `id_completedsurvey`, `id_surveytemplate`, `id_question`, `id_answer`) VALUES
(1, 1, 2, 1, 1),
(2, 1, 4, 2, 4),
(3, 1, 4, 2, 5),
(4, 1, 5, 3, 6),
(5, 1, 5, 3, 7),
(6, 1, 5, 3, 8),
(7, 1, 5, 3, 9),
(8, 1, 6, 4, 10),
(9, 1, 6, 4, 11);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `completedsurvey`
--

CREATE TABLE `completedsurvey` (
  `id_completedsurvey` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `id_survey` int(11) NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `completedsurvey`
--

INSERT INTO `completedsurvey` (`id_completedsurvey`, `id_user`, `id_survey`, `datetime`) VALUES
(1, 1, 2, '2018-07-05 20:02:08');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `possibleanswers`
--

CREATE TABLE `possibleanswers` (
  `id_answer` int(11) NOT NULL,
  `id_question` int(11) NOT NULL,
  `answerdescription` varchar(250) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `possibleanswers`
--

INSERT INTO `possibleanswers` (`id_answer`, `id_question`, `answerdescription`) VALUES
(1, 1, 'TAK'),
(3, 1, 'NIE'),
(4, 2, '0'),
(5, 2, '1'),
(6, 3, '0'),
(7, 3, '1'),
(8, 3, '2'),
(9, 3, '3'),
(10, 4, 'NIC'),
(11, 4, 'WSZYSTKO'),
(12, 4, 'CZESC'),
(13, 10, 'OK'),
(14, 10, 'NIE OK');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `questionbase`
--

CREATE TABLE `questionbase` (
  `id_question` int(11) NOT NULL,
  `question_description` varchar(250) NOT NULL,
  `id_questiontype` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `questionbase`
--

INSERT INTO `questionbase` (`id_question`, `question_description`, `id_questiontype`) VALUES
(1, 'To jest pytanie 1', 1),
(2, 'To jest pytanie 2', 2),
(3, 'To jest pytanie 3', 2),
(4, 'To jest pytanie 4', 2),
(5, 'To jest pytanie 5', 1),
(6, 'To jest pytanie 6', 1),
(7, 'To jest pytanie 7', 2),
(8, 'To jest pytanie 8', 1),
(9, 'To jest pytanie 9', 2),
(10, 'To jest pytanie 10', 1);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `questiontags`
--

CREATE TABLE `questiontags` (
  `id_questiontag` int(11) NOT NULL,
  `id_tag` int(11) NOT NULL,
  `id_question` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `questiontags`
--

INSERT INTO `questiontags` (`id_questiontag`, `id_tag`, `id_question`) VALUES
(2, 2, 2);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `questiontypes`
--

CREATE TABLE `questiontypes` (
  `id_questiontype` int(11) NOT NULL,
  `type_definition` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `questiontypes`
--

INSERT INTO `questiontypes` (`id_questiontype`, `type_definition`) VALUES
(1, 'jednkrotnego wyboru'),
(2, 'wielokrotnego wyboru');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `survey`
--

CREATE TABLE `survey` (
  `id_survey` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `survey_description` varchar(250) DEFAULT NULL,
  `datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `active` int(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `survey`
--

INSERT INTO `survey` (`id_survey`, `id_user`, `survey_description`, `datetime`, `active`) VALUES
(1, 1, 'ciekawa', '2018-07-04 19:15:47', 1),
(2, 1, 'To jest nasza pierwsza ankieta', '2018-04-14 21:11:19', 1);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `surveytemplate`
--

CREATE TABLE `surveytemplate` (
  `id_surveytemplate` int(11) NOT NULL,
  `id_survey` int(11) DEFAULT NULL,
  `id_question` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `surveytemplate`
--

INSERT INTO `surveytemplate` (`id_surveytemplate`, `id_survey`, `id_question`) VALUES
(2, 2, 1),
(4, 2, 2),
(5, 2, 3),
(6, 2, 4);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `tags`
--

CREATE TABLE `tags` (
  `id_tag` int(11) NOT NULL,
  `tag_description` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `tags`
--

INSERT INTO `tags` (`id_tag`, `tag_description`) VALUES
(2, 'studia');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `users`
--

CREATE TABLE `users` (
  `id_user` int(11) NOT NULL,
  `login` varchar(25) NOT NULL,
  `pass` varchar(25) NOT NULL,
  `email` varchar(50) NOT NULL,
  `Role` int(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `users`
--

INSERT INTO `users` (`id_user`, `login`, `pass`, `email`, `Role`) VALUES
(1, 'login', 'login', 'email@email.com', 1),
(2, 'login2', 'login2', 'login2@login1.com', 1);

--
-- Indeksy dla zrzutów tabel
--

--
-- Indexes for table `completedanswers`
--
ALTER TABLE `completedanswers`
  ADD PRIMARY KEY (`id_completedanswer`),
  ADD KEY `id_surveytemplate` (`id_surveytemplate`) USING BTREE,
  ADD KEY `id_answer` (`id_answer`),
  ADD KEY `id_question` (`id_question`),
  ADD KEY `id_surveycompleted` (`id_completedsurvey`) USING BTREE;

--
-- Indexes for table `completedsurvey`
--
ALTER TABLE `completedsurvey`
  ADD PRIMARY KEY (`id_completedsurvey`),
  ADD KEY `id_user` (`id_user`),
  ADD KEY `id_survey` (`id_survey`);

--
-- Indexes for table `possibleanswers`
--
ALTER TABLE `possibleanswers`
  ADD PRIMARY KEY (`id_answer`),
  ADD KEY `id_question` (`id_question`) USING BTREE;

--
-- Indexes for table `questionbase`
--
ALTER TABLE `questionbase`
  ADD PRIMARY KEY (`id_question`),
  ADD KEY `id_questiontype` (`id_questiontype`) USING BTREE;

--
-- Indexes for table `questiontags`
--
ALTER TABLE `questiontags`
  ADD PRIMARY KEY (`id_questiontag`),
  ADD KEY `id_tag` (`id_tag`),
  ADD KEY `id_queston` (`id_question`);

--
-- Indexes for table `questiontypes`
--
ALTER TABLE `questiontypes`
  ADD PRIMARY KEY (`id_questiontype`);

--
-- Indexes for table `survey`
--
ALTER TABLE `survey`
  ADD PRIMARY KEY (`id_survey`),
  ADD KEY `id_user` (`id_user`);

--
-- Indexes for table `surveytemplate`
--
ALTER TABLE `surveytemplate`
  ADD PRIMARY KEY (`id_surveytemplate`) USING BTREE,
  ADD KEY `id_surveytemplate` (`id_question`),
  ADD KEY `id_survey` (`id_survey`);

--
-- Indexes for table `tags`
--
ALTER TABLE `tags`
  ADD PRIMARY KEY (`id_tag`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id_user`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT dla tabeli `completedanswers`
--
ALTER TABLE `completedanswers`
  MODIFY `id_completedanswer` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT dla tabeli `completedsurvey`
--
ALTER TABLE `completedsurvey`
  MODIFY `id_completedsurvey` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT dla tabeli `possibleanswers`
--
ALTER TABLE `possibleanswers`
  MODIFY `id_answer` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT dla tabeli `questionbase`
--
ALTER TABLE `questionbase`
  MODIFY `id_question` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT dla tabeli `questiontags`
--
ALTER TABLE `questiontags`
  MODIFY `id_questiontag` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT dla tabeli `survey`
--
ALTER TABLE `survey`
  MODIFY `id_survey` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT dla tabeli `surveytemplate`
--
ALTER TABLE `surveytemplate`
  MODIFY `id_surveytemplate` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT dla tabeli `tags`
--
ALTER TABLE `tags`
  MODIFY `id_tag` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT dla tabeli `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `completedanswers`
--
ALTER TABLE `completedanswers`
  ADD CONSTRAINT `completedanswers_ibfk_4` FOREIGN KEY (`id_completedsurvey`) REFERENCES `completedsurvey` (`id_completedsurvey`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `completedanswers_ibfk_5` FOREIGN KEY (`id_answer`) REFERENCES `possibleanswers` (`id_answer`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ograniczenia dla tabeli `completedsurvey`
--
ALTER TABLE `completedsurvey`
  ADD CONSTRAINT `completedsurvey_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `completedsurvey_ibfk_2` FOREIGN KEY (`id_survey`) REFERENCES `survey` (`id_survey`) ON DELETE NO ACTION ON UPDATE NO ACTION;

--
-- Ograniczenia dla tabeli `possibleanswers`
--
ALTER TABLE `possibleanswers`
  ADD CONSTRAINT `possibleanswers_ibfk_1` FOREIGN KEY (`id_question`) REFERENCES `questionbase` (`id_question`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `questionbase`
--
ALTER TABLE `questionbase`
  ADD CONSTRAINT `questionbase_ibfk_1` FOREIGN KEY (`id_questiontype`) REFERENCES `questiontypes` (`id_questiontype`);

--
-- Ograniczenia dla tabeli `questiontags`
--
ALTER TABLE `questiontags`
  ADD CONSTRAINT `questiontags_ibfk_1` FOREIGN KEY (`id_tag`) REFERENCES `tags` (`id_tag`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `questiontags_ibfk_2` FOREIGN KEY (`id_question`) REFERENCES `questionbase` (`id_question`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `survey`
--
ALTER TABLE `survey`
  ADD CONSTRAINT `survey_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `surveytemplate`
--
ALTER TABLE `surveytemplate`
  ADD CONSTRAINT `surveytemplate_ibfk_1` FOREIGN KEY (`id_survey`) REFERENCES `survey` (`id_survey`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
