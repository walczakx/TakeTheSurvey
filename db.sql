-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Czas generowania: 14 Kwi 2018, 16:49
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
-- Struktura tabeli dla tabeli `completedsurvey`
--

CREATE TABLE `completedsurvey` (
  `id_completedsurvey` int(11) NOT NULL,
  `id_surveytemplate` int(11) NOT NULL,
  `id_question` int(11) NOT NULL,
  `id_answer` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `completedsurvey`
--

INSERT INTO `completedsurvey` (`id_completedsurvey`, `id_surveytemplate`, `id_question`, `id_answer`) VALUES
(1, 2, 1, 1),
(2, 4, 2, 4),
(3, 4, 2, 5),
(4, 5, 3, 6),
(5, 5, 3, 7),
(6, 5, 3, 8),
(7, 5, 3, 9),
(8, 6, 4, 10),
(9, 6, 4, 11);

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
(12, 4, 'CZESC');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `questionbase`
--

CREATE TABLE `questionbase` (
  `id_question` int(11) NOT NULL,
  `question_description` varchar(250) NOT NULL,
  `questiontype` int(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `questionbase`
--

INSERT INTO `questionbase` (`id_question`, `question_description`, `questiontype`) VALUES
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
  `id_question` int(11) DEFAULT NULL,
  `id_survey` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `questiontags`
--

INSERT INTO `questiontags` (`id_questiontag`, `id_tag`, `id_question`, `id_survey`) VALUES
(2, 2, 2, 2);

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `survey`
--

CREATE TABLE `survey` (
  `id_survey` int(11) NOT NULL,
  `id_user` int(11) NOT NULL,
  `survey_description` varchar(250) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `survey`
--

INSERT INTO `survey` (`id_survey`, `id_user`, `survey_description`) VALUES
(2, 1, 'To jest nasza pierwsza ankieta');

-- --------------------------------------------------------

--
-- Struktura tabeli dla tabeli `surveytemplate`
--

CREATE TABLE `surveytemplate` (
  `id_surveytemplate` int(11) NOT NULL,
  `id_question` int(11) DEFAULT NULL,
  `id_survey` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `surveytemplate`
--

INSERT INTO `surveytemplate` (`id_surveytemplate`, `id_question`, `id_survey`) VALUES
(2, 1, 2),
(4, 2, 2),
(5, 3, 2),
(6, 4, 2);

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
  `pass` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Zrzut danych tabeli `users`
--

INSERT INTO `users` (`id_user`, `login`, `pass`) VALUES
(1, 'login', 'login');

--
-- Indeksy dla zrzutów tabel
--

--
-- Indexes for table `completedsurvey`
--
ALTER TABLE `completedsurvey`
  ADD PRIMARY KEY (`id_completedsurvey`),
  ADD KEY `id_surveytemplate` (`id_surveytemplate`) USING BTREE,
  ADD KEY `id_answer` (`id_answer`),
  ADD KEY `id_question` (`id_question`);

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
  ADD PRIMARY KEY (`id_question`);

--
-- Indexes for table `questiontags`
--
ALTER TABLE `questiontags`
  ADD PRIMARY KEY (`id_questiontag`),
  ADD KEY `id_tag` (`id_tag`),
  ADD KEY `id_queston` (`id_question`),
  ADD KEY `id_survey` (`id_survey`);

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
-- AUTO_INCREMENT dla tabeli `completedsurvey`
--
ALTER TABLE `completedsurvey`
  MODIFY `id_completedsurvey` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT dla tabeli `possibleanswers`
--
ALTER TABLE `possibleanswers`
  MODIFY `id_answer` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

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
-- AUTO_INCREMENT dla tabeli `surveytemplate`
--
ALTER TABLE `surveytemplate`
  MODIFY `id_surveytemplate` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT dla tabeli `tags`
--
ALTER TABLE `tags`
  MODIFY `id_tag` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT dla tabeli `users`
--
ALTER TABLE `users`
  MODIFY `id_user` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Ograniczenia dla zrzutów tabel
--

--
-- Ograniczenia dla tabeli `completedsurvey`
--
ALTER TABLE `completedsurvey`
  ADD CONSTRAINT `completedsurvey_ibfk_1` FOREIGN KEY (`id_answer`) REFERENCES `possibleanswers` (`id_answer`),
  ADD CONSTRAINT `completedsurvey_ibfk_2` FOREIGN KEY (`id_question`) REFERENCES `questionbase` (`id_question`),
  ADD CONSTRAINT `completedsurvey_ibfk_3` FOREIGN KEY (`id_surveytemplate`) REFERENCES `surveytemplate` (`id_surveytemplate`);

--
-- Ograniczenia dla tabeli `possibleanswers`
--
ALTER TABLE `possibleanswers`
  ADD CONSTRAINT `possibleanswers_ibfk_1` FOREIGN KEY (`id_question`) REFERENCES `questionbase` (`id_question`);

--
-- Ograniczenia dla tabeli `questiontags`
--
ALTER TABLE `questiontags`
  ADD CONSTRAINT `questiontags_ibfk_1` FOREIGN KEY (`id_tag`) REFERENCES `tags` (`id_tag`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `questiontags_ibfk_2` FOREIGN KEY (`id_question`) REFERENCES `questionbase` (`id_question`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `questiontags_ibfk_3` FOREIGN KEY (`id_survey`) REFERENCES `survey` (`id_survey`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `survey`
--
ALTER TABLE `survey`
  ADD CONSTRAINT `survey_ibfk_1` FOREIGN KEY (`id_user`) REFERENCES `users` (`id_user`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Ograniczenia dla tabeli `surveytemplate`
--
ALTER TABLE `surveytemplate`
  ADD CONSTRAINT `surveytemplate_ibfk_1` FOREIGN KEY (`id_question`) REFERENCES `questionbase` (`id_question`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `surveytemplate_ibfk_2` FOREIGN KEY (`id_survey`) REFERENCES `survey` (`id_survey`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
